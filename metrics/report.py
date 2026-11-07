# Purpose: turn the JSON from collect.py into a quarterly coding-agent scorecard in
#          Markdown, with automatic warning signals and the metrics not to target.
# Book: Coding Agents in the Enterprise, Chapter 10
# Licence: MIT (see LICENSE)
"""Quarterly scorecard.

Run:
    python3 metrics/report.py examples/metrics.json --quarter 2026-Q3

Optional: --cost-per-month 81900 adds cost per merged PR. Use it only with an
org-wide collection, never with a single repository.

Signals (thresholds are starting points, tune them):
    review wait   agent median time to first review > human x 1.25
    PR size       agent median PR size > human x 1.5
    rework        agent rework rate > human rework rate + 2 points
"""

import argparse
import json


def fmt(value, kind):
    if value is None:
        return "n/a"
    if kind == "pct":
        return f"{value:.1%}"
    if kind == "h":
        return f"{value:.1f} h"
    return f"{value:,.0f}"


ROWS = [
    ("Merged PRs", "merged_prs", "n"),
    ("Median cycle time", "cycle_hours", "h"),
    ("Median time to first review", "first_review_hours", "h"),
    ("Median PR size (lines)", "size_lines", "n"),
    ("Rework rate (14 days)", "rework_rate", "pct"),
]


def signals(m):
    """Return warning lines comparing agent PRs with human PRs."""
    a, h = m["agent"], m["human"]
    out = []
    if a["first_review_hours"] and h["first_review_hours"] \
            and a["first_review_hours"] > 1.25 * h["first_review_hours"]:
        out.append("Agent PRs wait longer for review: add reviewers or cap agent PR volume.")
    if a["size_lines"] and h["size_lines"] and a["size_lines"] > 1.5 * h["size_lines"]:
        out.append("Agent PRs are much larger: enforce a PR size limit (Chapter 11).")
    if a["rework_rate"] is not None and h["rework_rate"] is not None \
            and a["rework_rate"] > h["rework_rate"] + 0.02:
        out.append("Agent PRs are reworked more often: tighten tests and review checklist.")
    return out or ["No warning signals this quarter."]


def render(m, quarter, cost_per_month=None):
    lines = [
        f"# Quarterly scorecard: {quarter}",
        "",
        f"Source: {m.get('source', 'n/a')}. Merged {m['since']} to {m['until'] or 'now'}.",
        f"Agent share of merged PRs: **{fmt(m['agent_share'], 'pct')}**.",
        "",
        "| Metric | Agent | Human | All |",
        "|---|--:|--:|--:|",
    ]
    for label, key, kind in ROWS:
        lines.append(f"| {label} | {fmt(m['agent'][key], kind)} | "
                     f"{fmt(m['human'][key], kind)} | {fmt(m['all'][key], kind)} |")
    detected = ", ".join(f"{k} {v}" for k, v in m.get("agent_detected_by", {}).items())
    lines += ["", f"Agent PRs detected by: {detected or 'none'}."]
    if cost_per_month and m["all"]["merged_prs"]:
        quarter_cost = 3 * cost_per_month
        per_pr = quarter_cost / m["all"]["merged_prs"]
        lines += ["", f"Cost per merged PR: ${per_pr:,.2f} (quarter cost ${quarter_cost:,.0f})."]
    lines += ["", "## Signals", ""] + [f"- {s}" for s in signals(m)]
    lines += [
        "",
        "## Not measured here",
        "",
        "- Change failure rate: join deploys to incidents (DORA).",
        "- Developer experience: quarterly survey (e.g. DX Core 4 or SPACE).",
        "- Security findings per PR: from your scanner.",
        "",
        "## Do not target",
        "",
        "- Agent share, PR counts or token spend per person.",
        "- Suggestion acceptance rates or usage leaderboards.",
        "",
        "Report them as context. Targets turn them into games.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("metrics", help="JSON written by collect.py")
    p.add_argument("--quarter", default="this quarter")
    p.add_argument("--cost-per-month", type=float)
    args = p.parse_args(argv)
    with open(args.metrics, encoding="utf-8") as handle:
        m = json.load(handle)
    print(render(m, args.quarter, args.cost_per_month), end="")


if __name__ == "__main__":
    main()
