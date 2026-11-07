# Quarterly scorecard: 2026-Q3

Source: sample-prs.json. Merged 2026-07-01 to 2026-10-01.
Agent share of merged PRs: **36.3%**.

| Metric | Agent | Human | All |
|---|--:|--:|--:|
| Merged PRs | 61 | 107 | 168 |
| Median cycle time | 21.4 h | 15.8 h | 17.4 h |
| Median time to first review | 6.9 h | 4.1 h | 4.9 h |
| Median PR size (lines) | 207 | 84 | 115 |
| Rework rate (14 days) | 16.4% | 7.5% | 10.7% |

Agent PRs detected by: author 16, branch 21, label 14, trailer 10.

## Signals

- Agent PRs wait longer for review: add reviewers or cap agent PR volume.
- Agent PRs are much larger: enforce a PR size limit (Chapter 11).
- Agent PRs are reworked more often: tighten tests and review checklist.

## Not measured here

- Change failure rate: join deploys to incidents (DORA).
- Developer experience: quarterly survey (e.g. DX Core 4 or SPACE).
- Security findings per PR: from your scanner.

## Do not target

- Agent share, PR counts or token spend per person.
- Suggestion acceptance rates or usage leaderboards.

Report them as context. Targets turn them into games.
