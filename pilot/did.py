# Purpose: difference-in-differences estimate of a coding-agent pilot's effect, with a
#          team-level bootstrap confidence interval, printed as Markdown.
# Book: Coding Agents in the Enterprise, Chapter 8
# Licence: MIT (see LICENSE)
"""Difference-in-differences (DiD) for a pilot.

Run:
    python3 pilot/did.py pilot/synthetic-pilot.csv --metric prs_per_engineer

How the maths works:
    team mean   = average of the metric over a team's weeks in one period
    group mean  = average of its team means (each team counts once)
    DiD effect  = (pilot group: pilot - baseline) - (comparison group: pilot - baseline)
The comparison group's change removes what would have happened anyway
(seasonality, a re-org, a new CI system). The 95% interval comes from a
bootstrap that resamples whole teams, because weeks within a team are not
independent.
"""

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
DEFAULT_CSV = HERE / "synthetic-pilot.csv"


def load(path, metric):
    """Return {group: {team: {period: team mean}}}."""
    values = defaultdict(list)
    groups = {}
    with open(path, encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            values[(row["team"], row["period"])].append(float(row[metric]))
            groups[row["team"]] = row["group"]
    teams = defaultdict(dict)
    for (team, period), vals in values.items():
        teams[team][period] = mean(vals)
    out = defaultdict(dict)
    for team, periods in teams.items():
        if {"baseline", "pilot"} - periods.keys():
            raise ValueError(f"team {team} needs both baseline and pilot weeks")
        out[groups[team]][team] = periods
    if {"pilot", "comparison"} - out.keys():
        raise ValueError("data needs both a pilot and a comparison group")
    return out


def group_means(teams):
    return (mean(t["baseline"] for t in teams), mean(t["pilot"] for t in teams))


def did(data):
    """Return the DiD effect and the four group means."""
    pb, pp = group_means(list(data["pilot"].values()))
    cb, cp = group_means(list(data["comparison"].values()))
    return {"effect": (pp - pb) - (cp - cb), "pilot": (pb, pp), "comparison": (cb, cp)}


def bootstrap(data, reps=2000, seed=43):
    """Return a 95% percentile interval by resampling teams within each group."""
    rng = random.Random(seed)
    pilot = list(data["pilot"].values())
    comp = list(data["comparison"].values())
    effects = []
    for _ in range(reps):
        sample = {"pilot": dict(enumerate(rng.choices(pilot, k=len(pilot)))),
                  "comparison": dict(enumerate(rng.choices(comp, k=len(comp))))}
        effects.append(did(sample)["effect"])
    effects.sort()
    return effects[int(0.025 * reps)], effects[int(0.975 * reps) - 1]


def render(data, metric, reps):
    r = did(data)
    low, high = bootstrap(data, reps)
    pb, pp = r["pilot"]
    cb, cp = r["comparison"]
    lines = [
        f"# Pilot analysis: {metric}",
        "",
        f"Teams: {len(data['pilot'])} pilot, {len(data['comparison'])} comparison.",
        "",
        "| Group | Baseline | Pilot | Change |",
        "|---|--:|--:|--:|",
        f"| Pilot teams | {pb:.2f} | {pp:.2f} | {pp - pb:+.2f} |",
        f"| Comparison teams | {cb:.2f} | {cp:.2f} | {cp - cb:+.2f} |",
        "",
        "| Result | Value |",
        "|---|--:|",
        f"| Naive before/after (pilot only) | {pp - pb:+.2f} |",
        f"| Difference-in-differences | {r['effect']:+.2f} |",
        f"| 95% CI (team bootstrap, {reps} reps) | {low:+.2f} to {high:+.2f} |",
        f"| Effect vs pilot baseline | {r['effect'] / pb:+.1%} |",
        "",
        "The naive figure includes the change the comparison teams also saw.",
        "If the interval includes zero, do not claim an effect.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="?", default=DEFAULT_CSV)
    p.add_argument("--metric", default="prs_per_engineer")
    p.add_argument("--reps", type=int, default=2000)
    args = p.parse_args(argv)
    print(render(load(args.csv, args.metric), args.metric, args.reps), end="")


if __name__ == "__main__":
    main()
