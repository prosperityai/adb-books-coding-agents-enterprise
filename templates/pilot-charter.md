<!--
Purpose: one-page charter for a controlled coding-agent pilot.
Book: Coding Agents in the Enterprise, Chapter 8 and Appendix A
Licence: MIT (see LICENSE)
-->

# Pilot charter: [tool(s)] at [organisation]

| Field | Entry |
|---|---|
| Sponsor | [executive] |
| Pilot lead | [name] |
| Analyst | [name, independent of the vendor] |
| Dates | Baseline [from-to]; pilot [from-to] |
| Budget cap | [$ total], alert at [x]% |

## Question

Does [tool] change [primary metric] for [type of team/work], at what cost,
and without making quality or security worse?

## Design

- **Pilot teams:** [list, n engineers]. **Comparison teams:** [list, n].
- Teams were matched on [size, domain, baseline output] before assignment.
- Sample size from `pilot/sample_size.py`: [n teams per group] for an effect
  of [x] with 80% power.
- Analysis: difference-in-differences (`pilot/did.py`), team-level bootstrap.

## Metrics

| Type | Metric | Source |
|---|---|---|
| Primary | [Merged PRs per engineer per week] | GitHub |
| Speed | Cycle time, time to first review | GitHub |
| Quality | Rework rate, change failure rate | GitHub, incidents |
| Security | Findings per PR, secrets caught | Scanners, hooks |
| Cost | Spend per engineer, per merged PR | Vendor, gateway |
| People | Trust, time saved, frustration | Survey |

Not targets: acceptance rate, lines of code, usage rankings.

## Guardrails in force

Managed settings version [x]; hooks; sandbox and allowlist; no production
credentials; branch protection; AI code review checklist.

## Stop rules

Pause if: Sev 1 incident; spend above cap; review wait doubles for two weeks.

## Decision

Go / extend / stop, using the rule agreed in the 30-60-90 plan. Results are
shared with all participants, including null results.

## Ethics and privacy

Participation is [voluntary / assigned]. Data is reported at team level.
Individual data is not used in performance reviews.

**Signed:** Sponsor [ ] · CISO [ ] · Finance [ ] · Pilot lead [ ]
