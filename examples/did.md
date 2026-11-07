# Pilot analysis: prs_per_engineer

Teams: 6 pilot, 6 comparison.

| Group | Baseline | Pilot | Change |
|---|--:|--:|--:|
| Pilot teams | 2.28 | 2.91 | +0.63 |
| Comparison teams | 2.38 | 2.62 | +0.24 |

| Result | Value |
|---|--:|
| Naive before/after (pilot only) | +0.63 |
| Difference-in-differences | +0.39 |
| 95% CI (team bootstrap, 2000 reps) | +0.32 to +0.46 |
| Effect vs pilot baseline | +17.1% |

The naive figure includes the change the comparison teams also saw.
If the interval includes zero, do not claim an effect.
