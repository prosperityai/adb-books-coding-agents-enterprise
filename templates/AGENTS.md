<!--
Purpose: AGENTS.md template (read by Codex, Copilot coding agent, Cursor and others).
Book: Coding Agents in the Enterprise, Chapter 7 and Appendix A
Licence: MIT (see LICENSE)
Keep it short. Put rules for one folder in an AGENTS.md inside that folder;
the nearest file to the code being changed applies. Delete these comments.
-->

# AGENTS.md

## Project

[One paragraph: what this service does, who uses it, what must never break.]

## Commands

- Install: `[make install]`
- Test all: `[make test]`
- Test one file: `[pytest tests/test_x.py -q]`
- Lint and format: `[make lint]`
- Run locally: `[make run]`

Run the tests and the linter before you say a task is done.

## Layout

- `[src/payments/]` payment logic. Owned by [team].
- `[src/api/]` HTTP handlers only; no business logic here.
- `[tests/]` mirrors `src/`.
- Do not edit `[generated/]` or `[vendor/]`.

## Conventions

- [Language and version, e.g. Python 3.13, type hints required.]
- [Error handling rule, e.g. raise domain errors, never return None for failure.]
- [Money: integers in minor units, never floats.]
- Reuse helpers in `[src/common/]` before writing new ones.

## Boundaries

- Never read or write `.env` files, `secrets/`, or credentials.
- Never change CI workflows, security settings or dependency pins unless the
  task says so.
- Do not add a dependency without saying why in the PR description.
- Keep each PR under [400] changed lines. Split larger work.

## Pull requests

- Title: `[type]: [short summary]`. Link the issue.
- Describe what changed, why, and how you tested it.
- Add the `agent-authored` label.
