<!--
Purpose: one-page business case for a coding-agent rollout, without overclaiming.
Book: Coding Agents in the Enterprise, Chapter 2 and Appendix A
Licence: MIT (see LICENSE)
-->

# Business case: AI coding agents at [organisation]

**Ask:** approve [$ annual] for [tools] for [n] engineers, for [12] months,
with a go/no-go review after a [90]-day pilot.

## Problem

[Two sentences: the delivery problem we want to solve, with today's numbers,
e.g. "Median cycle time is 4.2 days; the modernisation backlog is 18 months."]

## Evidence (honest range)

- Controlled studies and large field data show individual output up 20-26%
  (Google RCT, Cui et al., Microsoft field study).
- Some trials found experienced developers slower (METR 2025).
- Organisation-level delivery gains are not automatic: review time and
  instability can rise (Faros 2025, DORA 2025).
- We assume [15]% more merged PRs, below the published field results.

## Cost (from `cost/cost_model.py`)

| Item | Per month |
|---|--:|
| Tools (seats + metered usage) | [$] |
| Platform (gateway, logging, scanning) | [$] |
| Enablement (people, training) | [$] |
| **Total** | **[$]** |

Cost per engineer: [$] per month. Cost per merged PR: [$].

## Break-even

The rollout pays for itself if each engineer saves [x] hours a month
(total monthly cost / loaded hourly cost / engineers). Surveys report
[3-4] hours a week saved, but self-reports overstate; we will measure.

## Risks and controls

| Risk | Control |
|---|---|
| Security incidents, leaked secrets | Guardrail baseline, hooks, sandbox |
| Review bottleneck, bigger PRs | PR size limit, review checklist |
| Cost overrun | Spend caps, alerts, monthly review |
| Skill loss in juniors | Skills-protection plan |
| Vendor lock-in or policy change | Multi-tool strategy, gateway |

## How we will know

Pilot with comparison teams; difference-in-differences on [metric]; quarterly
scorecard. We will report null or negative results.

## Decision needed

[Approve pilot budget of $x / approve full rollout / defer], by [date].
