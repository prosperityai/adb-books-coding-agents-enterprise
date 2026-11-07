#!/usr/bin/env python3
# Purpose: PostToolUse hook that appends one JSON line per agent tool call to an audit
#          log, for shipping to the SIEM. Never blocks and never logs file content.
# Book: Coding Agents in the Enterprise, Chapter 5
# Licence: MIT (see LICENSE)
"""Append an audit record for each tool call.

Log file: $AGENT_AUDIT_LOG, default ~/.claude/audit/agent-audit.jsonl.
Each line: time (UTC), user, host, session, event, tool, cwd and a short
summary (the command, or the file path). File content is never logged, because
it can contain secrets. Ship the file to the SIEM with your usual log agent.

Exit code is always 0: an audit hook must not break the developer's session.
For the authoritative record, also export OpenTelemetry from the tool itself.
"""

import datetime as dt
import getpass
import json
import os
import socket
import sys
from pathlib import Path

MAX_SUMMARY = 300


def summary(event):
    tool_input = event.get("tool_input", {}) or {}
    for key in ("command", "file_path", "notebook_path", "url", "pattern", "path"):
        if tool_input.get(key):
            return str(tool_input[key])[:MAX_SUMMARY]
    return ""


def record(event):
    return {
        "time": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "user": getpass.getuser(),
        "host": socket.gethostname(),
        "session": event.get("session_id"),
        "event": event.get("hook_event_name"),
        "tool": event.get("tool_name"),
        "cwd": event.get("cwd"),
        "summary": summary(event),
    }


def log_path():
    default = Path.home() / ".claude" / "audit" / "agent-audit.jsonl"
    return Path(os.environ.get("AGENT_AUDIT_LOG", default))


def main():
    try:
        event = json.load(sys.stdin)
        path = log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record(event)) + "\n")
    except Exception as exc:  # noqa: BLE001 - never break the session
        print(f"audit hook: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
