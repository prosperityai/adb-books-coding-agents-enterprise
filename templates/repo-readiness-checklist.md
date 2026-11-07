<!--
Purpose: check a repository is ready for coding agents before a team turns them on.
Book: Coding Agents in the Enterprise, Chapter 7 and Appendix A
Licence: MIT (see LICENSE)
-->

# Repository readiness checklist

**Repository:** [ ] · **Owner:** [ ] · **Score:** [ ] / 20

Score 1 for each item met. Below 12: fix the basics before piloting agents
here. Agents amplify what is there, good or bad.

## Build and test (the agent's safety net)

- [ ] One command builds the project from a clean checkout
- [ ] One command runs the tests, in under [10] minutes
- [ ] Tests pass reliably (no known flaky tests)
- [ ] Coverage on critical paths is known and acceptable
- [ ] Linter and formatter run in one command and in CI
- [ ] Type checking (where the language supports it)

## Instructions for agents

- [ ] `AGENTS.md` at the root: commands, layout, conventions, boundaries
- [ ] Folder-level rules where a folder differs (scoped, not global)
- [ ] `CLAUDE.md` or tool-specific file points to `AGENTS.md`
- [ ] Architecture notes or ADRs an agent can read

## Change hygiene

- [ ] Branch protection and required review on the default branch
- [ ] PR template asks what changed, why, and how it was tested
- [ ] PR size limit agreed (e.g. 400 lines)
- [ ] CODEOWNERS for sensitive areas

## Security

- [ ] No secrets in the repository or its history (scanned)
- [ ] `.env` and secret paths in `.gitignore` and agent deny rules
- [ ] Dependencies pinned; lockfile committed
- [ ] SAST and secret scanning in CI

## Environment

- [ ] Dev container or setup script installs everything without manual steps
- [ ] Local and CI runs need no production credentials

## Notes

| Gap | Fix | Owner | Due |
|---|---|---|---|
| | | | |
