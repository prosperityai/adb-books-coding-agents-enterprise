# Purpose: how many engineers (and teams) a coding-agent pilot needs to detect a given
#          change in a metric such as merged PRs per engineer per week.
# Book: Coding Agents in the Enterprise, Chapter 8
# Licence: MIT (see LICENSE)
"""Pilot sample-size calculator (two-sample, two-sided, normal approximation).

Run:
    python3 pilot/sample_size.py --sd 1.2 --effect 0.4 --team-size 8 --icc 0.10

How the maths works:
    n per group = 2 x (z[1 - alpha/2] + z[power])^2 x sd^2 / effect^2   (rounded up)
    If engineers are assigned by team, people in a team are alike, so each
    extra person adds less information. Inflate by the design effect:
    design effect = 1 + (team size - 1) x ICC
    teams per group = ceil(n per group x design effect / team size)
ICC (intra-cluster correlation) is the share of variance between teams.
Estimate SD and ICC from your own baseline data, not from this example.
"""

import argparse
import math
from statistics import NormalDist


def per_group(sd, effect, alpha=0.05, power=0.80):
    """Engineers per group for an individually randomised pilot."""
    if sd <= 0 or effect <= 0:
        raise ValueError("sd and effect must be positive")
    z = NormalDist().inv_cdf
    n = 2 * (z(1 - alpha / 2) + z(power)) ** 2 * sd**2 / effect**2
    return math.ceil(n)


def clustered(n, team_size, icc):
    """Return (design effect, engineers per group, teams per group) for team assignment."""
    if team_size < 1 or not 0 <= icc <= 1:
        raise ValueError("team_size must be >= 1 and icc between 0 and 1")
    deff = 1 + (team_size - 1) * icc
    teams = math.ceil(n * deff / team_size)
    return deff, teams * team_size, teams


def render(args):
    n = per_group(args.sd, args.effect, args.alpha, args.power)
    deff, engineers, teams = clustered(n, args.team_size, args.icc)
    lines = [
        "# Pilot sample size",
        "",
        "| Input | Value |",
        "|---|--:|",
        f"| Metric SD (per engineer) | {args.sd} |",
        f"| Smallest effect worth detecting | {args.effect} |",
        f"| Effect as share of SD | {args.effect / args.sd:.2f} |",
        f"| Alpha (two-sided) | {args.alpha} |",
        f"| Power | {args.power:.0%} |",
        f"| Team size | {args.team_size} |",
        f"| ICC | {args.icc} |",
        "",
        "| Result | Per group | Both groups |",
        "|---|--:|--:|",
        f"| Engineers, assigned one by one | {n} | {2 * n} |",
        f"| Engineers, assigned by team | {engineers} | {2 * engineers} |",
        f"| Teams, assigned by team | {teams} | {2 * teams} |",
        "",
        f"Design effect: {deff:.2f}. Assigning whole teams costs "
        f"{engineers - n} extra engineers per group.",
        "Use several baseline weeks per engineer to cut the SD, and check the",
        "groups are balanced on baseline output before the pilot starts.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--sd", type=float, default=1.2, help="SD of the metric per engineer")
    p.add_argument("--effect", type=float, default=0.4, help="smallest change worth detecting")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float, default=0.80)
    p.add_argument("--team-size", type=int, default=8)
    p.add_argument("--icc", type=float, default=0.10)
    print(render(p.parse_args(argv)), end="")


if __name__ == "__main__":
    main()
