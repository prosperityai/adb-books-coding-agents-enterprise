<!--
Purpose: checklist for reviewing agent-written pull requests.
Book: Coding Agents in the Enterprise, Chapter 11 and Appendix A
Licence: MIT (see LICENSE)
-->

# AI code review checklist

Use for every PR labelled `agent-authored`. A human reviewer owns the merge.

## Before you read the code

- [ ] The PR links to an issue or spec that says what "done" means.
- [ ] The PR is small enough to review properly ([400] lines or less). If not,
      send it back to be split.
- [ ] CI is green: tests, lint, type checks, SAST, secret scan, licence scan.
- [ ] The author (human) has reviewed it first and says so in the description.

## Correctness

- [ ] It solves the stated problem, not a nearby one.
- [ ] Edge cases are handled: empty input, nulls, limits, time zones, money
      rounding, concurrency.
- [ ] Error handling is real, not swallowed or logged and ignored.
- [ ] No invented APIs, config keys or functions. Check anything unfamiliar.

## Tests

- [ ] New behaviour has tests that would fail without the change.
- [ ] Tests were not deleted, skipped or weakened to make CI pass.
- [ ] Assertions check results, not just that code ran.

## Security

- [ ] No secrets, tokens or keys in code, tests, fixtures or logs.
- [ ] Inputs are validated; queries are parameterised; output is encoded (XSS).
- [ ] New dependencies exist, are the intended package (not a look-alike) and
      are pinned. Check for "slopsquatting".
- [ ] No new network calls, file writes or permissions without a reason.
- [ ] Authentication and authorisation checks are unchanged or reviewed by
      the owning team.

## Maintainability

- [ ] No copy-paste duplication of existing helpers. Reuse, do not re-create.
- [ ] Names and structure match the codebase's conventions (AGENTS.md).
- [ ] No dead code, commented-out code or stray debug output.
- [ ] Comments explain why, not what.

## Ownership

- [ ] A named human can explain how this code works.
- [ ] Docs, runbooks and changelogs are updated if behaviour changed.

## Verdict

- Approve / Request changes / Reject and re-scope.
- If rejected, note why in the PR so the prompt or rules file can improve.
