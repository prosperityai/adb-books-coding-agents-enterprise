# Purpose: generate the synthetic pilot dataset (pilot vs comparison teams, baseline vs
#          pilot weeks) used by did.py. Seeded, so the output is identical on every run.
# Book: Coding Agents in the Enterprise, Chapter 8
# Licence: MIT (see LICENSE)
"""Write pilot/synthetic-pilot.csv.

Run:
    python3 pilot/make_synthetic.py

The data is invented. Built in: a common trend of +0.15 PRs/engineer/week for
everyone in the pilot period, and a true pilot effect of +0.45 for pilot teams.
A good analysis should recover roughly +0.45, not +0.60.
"""

import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "synthetic-pilot.csv"
SEED = 43
TEAMS_PER_GROUP = 6
BASELINE_WEEKS = 8
PILOT_WEEKS = 8
TREND = 0.15
TRUE_EFFECT = 0.45
FIELDS = ["team", "group", "period", "week", "engineers", "merged_prs",
          "prs_per_engineer", "median_cycle_hours"]


def generate(seed=SEED):
    """Return the list of weekly rows."""
    rng = random.Random(seed)
    rows = []
    for group in ("pilot", "comparison"):
        for t in range(1, TEAMS_PER_GROUP + 1):
            team = f"{group[0].upper()}{t:02d}"
            engineers = rng.randint(6, 10)
            team_level = rng.gauss(2.4, 0.35)       # team's usual PRs/engineer/week
            cycle = rng.gauss(30, 5)                # team's usual cycle time, hours
            for week in range(1, BASELINE_WEEKS + PILOT_WEEKS + 1):
                in_pilot = week > BASELINE_WEEKS
                rate = team_level + rng.gauss(0, 0.30)
                hours = cycle + rng.gauss(0, 4)
                if in_pilot:
                    rate += TREND
                    if group == "pilot":
                        rate += TRUE_EFFECT
                        hours *= 0.9
                merged = max(0, round(rate * engineers))
                rows.append({
                    "team": team,
                    "group": group,
                    "period": "pilot" if in_pilot else "baseline",
                    "week": week,
                    "engineers": engineers,
                    "merged_prs": merged,
                    "prs_per_engineer": f"{merged / engineers:.3f}",
                    "median_cycle_hours": f"{max(hours, 1):.1f}",
                })
    return rows


def write(rows, path=OUT):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    write(generate())
    print(f"Wrote {OUT.name}")
