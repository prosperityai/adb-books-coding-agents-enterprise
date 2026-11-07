# Policies as code (Chapter 5)

> **Client-side controls are not a security boundary.** Everything in this
> folder runs on the developer's machine or in the agent's environment, and a
> determined user or a clever prompt injection can get round parts of it.
> Anthropic says this of its own managed settings. Use these files to make the
> safe path the default, and keep the real boundaries elsewhere: least-privilege
> credentials, no production access from dev machines, branch protection,
> network egress controls, and review.

Every key was checked against the vendor's documentation or source code on
7 Nov 2026 (see the table at the end). Tools change fast: check again before
you deploy.

## Contents

| Path | What it is |
|---|---|
| `claude-code/managed-settings.json` | Claude Code organisation policy |
| `hooks/block_secrets_and_destructive.py` | PreToolUse hook: blocks risky calls |
| `hooks/audit_log.py` | PostToolUse hook: JSONL audit trail |
| `codex/config.toml` | Codex defaults users may change |
| `codex/requirements.toml` | Codex limits users cannot change |
| `copilot/copilot-setup-steps.yml` | Copilot coding agent environment |
| `cursor/hooks.json` | Cursor enterprise hook using the same script |

## Claude Code

Deploy `managed-settings.json` by MDM to the system directory
(`/Library/Application Support/ClaudeCode/` on macOS, `/etc/claude-code/` on
Linux and WSL, `C:\Program Files\ClaudeCode\` on Windows), or paste the same
JSON into server-managed settings in the claude.ai admin console. Only
server-managed settings reach cloud sessions. Copy the two hook scripts to
`/etc/claude-code/hooks/` (or change the paths).

What the file does:

- `permissions.deny` stops reads of `.env`, `secrets/`, SSH and AWS files, and
  `curl`, `wget`, `rm -rf` and force-push commands *as Claude writes them*.
  Rules match the text, so `git -C . push --force` slips past the rules, and
  past the example hook too (its pattern expects `git push`). Pattern matching
  is a speed bump, not a boundary: server-side branch protection is what
  actually stops a force push.
- `disableBypassPermissionsMode: "disable"` removes the bypass mode.
- `allowManagedPermissionRulesOnly` and `allowManagedHooksOnly` make the
  managed rules and hooks the only ones that apply.
- `allowedMcpServers` matches servers by URL, never by name: a user can name
  any server "github". With `allowManagedMcpServersOnly`, user allowlists are
  ignored. Deny always wins over allow.
- `sandbox` runs commands in the OS sandbox, refuses to start without it, and
  limits network access to the listed domains.
- `cleanupPeriodDays: 14` deletes local transcripts after two weeks.

Telemetry: send OpenTelemetry to your collector by setting the exporter
variables in managed settings (see the Claude Code monitoring page). They are
left out here because the endpoint is yours to choose.

Not available: different policies per group in server-managed settings.
Deploy different files to different device groups instead.

## The hooks

Test them by hand:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' \
  | python3 policies/hooks/block_secrets_and_destructive.py; echo "exit $?"
```

Exit code 2 blocks and sends stderr to the agent; 0 lets the normal
permission rules decide. The audit hook never blocks and never logs file
content. Set `AGENT_AUDIT_LOG` to change where it writes.

## OpenAI Codex

`config.toml` sets defaults: workspace-write sandbox, approval on request, no
network for agent commands, no web search, core environment variables only, no
local prompt history, OpenTelemetry with prompts redacted.

`requirements.toml` enforces limits: no full-access sandbox, no
never-ask approval, managed hooks only, forbidden `rm -rf` and force push,
blocked reads of credential folders, and an MCP allowlist by URL prefix.
Command rules match prefixes literally, so they are a backstop, not a wall.

## GitHub Copilot coding agent

- Enable the agent per organisation under Copilot policies; limit it to
  pilot organisations first.
- Firewall: Settings, Copilot, Internet access (repository or organisation).
  Keep **Enable firewall** on, use the **Recommended allowlist**, and add
  only the package mirrors you need. A domain entry also allows its
  subdomains; a URL entry allows only that path and below.
- The firewall covers processes the agent starts with its Bash tool only. It
  does not cover MCP server processes, and GitHub says it is not a
  comprehensive security solution. It does not work with self-hosted or
  Windows runners.
- `copilot-setup-steps.yml` installs dependencies before the agent starts,
  which keeps the allowlist short.
- Content exclusions: check whether they apply to the cloud agent for your
  plan before you rely on them; the research for this book found this unclear.

## Cursor

- `cursor/hooks.json` goes in the enterprise location
  (`/Library/Application Support/Cursor/hooks.json`, `/etc/cursor/hooks.json`,
  `C:\ProgramData\Cursor\hooks.json`) or the team dashboard (Enterprise).
- It runs the same blocking script on `beforeShellExecution`. Exit 2 blocks,
  and `failClosed: true` blocks if the hook itself fails.
- Also, in the admin dashboard: enforce Privacy Mode, restrict models,
  restrict who can create Cloud Agents, and manage trusted MCP servers. These
  are dashboard settings, not files, so they are not shown here.
- File-read and edit hooks exist (`beforeReadFile`, `afterFileEdit`), but
  their input fields were not checked for this edition, so they are not used.

## Where each key was verified (7 Nov 2026)

| Tool | Source |
|---|---|
| Claude Code settings | code.claude.com/docs/en/settings-example.md |
| Claude Code MCP lists | code.claude.com/docs/ko/managed-mcp |
| Claude Code hooks | code.claude.com/docs/en/hooks.md, hooks-guide.md |
| Codex config | openai/codex: codex-rs/core/config.schema.json |
| Codex requirements | openai/codex: codex-rs/config/src |
| Copilot setup steps | docs.github.com (customize-the-agent-environment) |
| Copilot firewall | docs.github.com (customize-the-firewall) |
| Cursor hooks | cursor.com/docs/agent/hooks |
