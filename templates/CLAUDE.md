<!--
Purpose: CLAUDE.md template for Claude Code, scoped to one repository or folder.
Book: Coding Agents in the Enterprise, Chapter 7 and Appendix A
Licence: MIT (see LICENSE)
Claude Code reads CLAUDE.md from the repo root and from subfolders it works in.
Keep the root file short and import AGENTS.md (@AGENTS.md) so rules live in one place.
Move long, task-specific guidance into skills, loaded only when needed.
Delete these comments.
-->

# CLAUDE.md

@AGENTS.md

The import above loads `AGENTS.md` (commands, layout and boundaries for this
repository). This file only adds what is specific to Claude Code.

## Working style

- For anything bigger than a one-file change, write a short plan first and
  wait for approval.
- Work test-first: write or update a failing test, then make it pass.
- Run `[make test]` and `[make lint]` before you finish. Show the result.
- Stop and ask if a task needs a new dependency, a schema change or access to
  anything outside this repository.

## This folder

<!-- In a subfolder CLAUDE.md, replace with rules for that folder only. -->
- [e.g. `src/ledger/`: every change needs a migration test; see `docs/ledger.md`.]

## Never

- Read `.env`, `secrets/` or credential files (blocked by policy anyway).
- Commit directly to `main` or push with `--force`.
- Mark a task done while tests fail.
