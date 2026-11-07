# Cost model: Example Bank (400 engineers)

All prices are assumptions as of Nov 2026. Verify before use.

## Tools (per month)

| Tool | Seats | Seat cost | Total |
|---|--:|--:|--:|
| Copilot Enterprise | 400 | $15,600 | $15,600 |
| Claude Code Enterprise | 120 | $2,400 | $21,120 |
| Cursor Teams | 40 | $1,200 | $1,680 |

Total = seat cost + usage above the included allowance.

| Tool | Avg usage/user | Metered | Overage |
|---|--:|--:|--:|
| Copilot Enterprise | $30 | $12,000 | $0 |
| Claude Code Enterprise | $156 | $18,720 | $18,720 |
| Cursor Teams | $12 | $480 | $480 |

## Monthly total

| Item | Per month |
|---|--:|
| Tools | $38,400 |
| LLM gateway hosting and support | $1,500 |
| Telemetry and SIEM ingestion | $800 |
| Extra code-scanning capacity | $1,200 |
| Platform engineer (1.0 FTE) | $15,000 |
| Champions (8 at 5% time) | $6,000 |
| Training (6 h each, spread over 12 months) | $19,000 |
| **Total** | **$81,900** |

## Headline figures

| Measure | Value |
|---|--:|
| Monthly total | $81,900 |
| Annual total | $982,800 |
| Cost per engineer per month | $205 |
| Merged PRs per month (assumed) | 4,600 |
| Cost per merged PR | $17.80 |
| Cost per extra PR from uplift | $136.50 |
| Break-even, engineer-hours/month | 862 |
| Break-even, hours/engineer/month | 2.2 |

Uplift assumed: 15% more merged PRs on a baseline of 10 per engineer per month.
Break-even uses a loaded cost of $95 per engineer-hour.
