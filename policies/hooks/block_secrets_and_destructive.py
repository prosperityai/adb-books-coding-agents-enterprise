#!/usr/bin/env python3
# Purpose: PreToolUse hook that blocks destructive shell commands, writes to .env files
#          and secrets in file content. Exit code 2 blocks; the reason goes to stderr.
# Book: Coding Agents in the Enterprise, Chapter 5
# Licence: MIT (see LICENSE)
"""Block dangerous agent tool calls before they run.

Reads one tool-call JSON object on stdin. Understands two shapes:
  Claude Code PreToolUse:   {"tool_name": "Bash", "tool_input": {"command": "..."}}
                            {"tool_name": "Write", "tool_input": {"file_path": "...",
                                                                  "content": "..."}}
  Cursor beforeShellExecution: {"command": "...", "cwd": "..."}

Exit 0 = no objection (normal permission rules still apply).
Exit 2 = block; stderr explains why (Claude Code and Cursor both treat 2 as block).
Unreadable input also exits 2: a security hook should fail closed.

This is a seatbelt, not a security boundary. Pattern matching can be evaded
(aliases, scripts, encodings). Pair it with sandboxing and least privilege.
"""

import json
import re
import sys
from pathlib import PurePath

SHELL_RULES = [
    (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b", "recursive force delete (rm -rf)"),
    (r"\brm\s+(-[a-zA-Z]+\s+)*(-r|-R|--recursive)\s+(-[a-zA-Z]+\s+)*(-f|--force)\b",
     "recursive force delete (rm -r -f)"),
    (r"\brm\s+(-[a-zA-Z]+\s+)*(-f|--force)\s+(-[a-zA-Z]+\s+)*(-r|-R|--recursive)\b",
     "recursive force delete (rm -f -r)"),
    (r"\bgit\s+push\b.*(\s--force(-with-lease)?\b|\s-f\b|\s\+\S+)",
     "force push (git push --force)"),
    (r"\bdrop\s+(table|database|schema)\b", "SQL DROP TABLE/DATABASE/SCHEMA"),
    (r"\btruncate\s+table\b", "SQL TRUNCATE TABLE"),
    (r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", "piping a download into a shell"),
    (r"\b(ba|z)?sh\s+<\(\s*(curl|wget)\b", "running a downloaded script"),
    (r"(>>?|\btee\s+(-a\s+)?)\s*\S*\.env(\.[\w.-]+)?(\s|$)", "writing to a .env file"),
]

SECRET_RULES = [
    (r"AKIA[0-9A-Z]{16}", "an AWS access key ID"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{36,}\b", "a GitHub token"),
    (r"\bxox[abpr]-[A-Za-z0-9-]{10,}", "a Slack token"),
]

ENV_TEMPLATES = {".env.example", ".env.sample", ".env.template"}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def is_env_file(path):
    name = PurePath(path).name
    return (name == ".env" or name.startswith(".env.")) and name not in ENV_TEMPLATES


def check_command(command):
    """Return a reason to block a shell command, or None."""
    for pattern, reason in SHELL_RULES:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            if reason == "writing to a .env file" and not is_env_file(match.group(0).split()[-1]
                                                                       .lstrip(">")):
                continue
            return reason
    return None


def check_write(tool_input):
    """Return a reason to block a file write or edit, or None."""
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if path and is_env_file(path):
        return f"writing to {PurePath(path).name}"
    text = " ".join(str(tool_input.get(k, "")) for k in ("content", "new_string", "new_source"))
    for edit in tool_input.get("edits", []) or []:
        text += " " + str(edit.get("new_string", ""))
    for pattern, reason in SECRET_RULES:
        if re.search(pattern, text):
            return f"content contains {reason}"
    return None


def decide(event):
    """Return a reason to block this tool call, or None to allow it."""
    if "tool_name" not in event and "command" in event:          # Cursor shell hook
        return check_command(str(event["command"]))
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input", {}) or {}
    if tool == "Bash":
        return check_command(str(tool_input.get("command", "")))
    if tool in WRITE_TOOLS:
        return check_write(tool_input)
    return None


def main():
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("expected a JSON object")
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Blocked by policy hook: could not read tool call ({exc}).", file=sys.stderr)
        return 2
    reason = decide(event)
    if reason:
        print(f"Blocked by Example Bank policy: {reason}. "
              "Ask a human to run this if it is really needed.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
