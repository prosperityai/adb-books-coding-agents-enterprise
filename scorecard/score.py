# Purpose: rank coding-agent tools on weighted, vendor-neutral criteria, disqualifying
#          any tool that misses a must-have gate, and print the ranking as Markdown.
# Book: Coding Agents in the Enterprise, Chapter 3
# Licence: MIT (see LICENSE)
"""Weighted vendor scorecard.

Run:
    python3 scorecard/score.py scorecard/example-scores.yaml

How the maths works (scores are 0-4, weights are points out of 100):
    weighted score = sum(weight x score) / (sum(weights) x 4) x 100   -> 0 to 100
    a tool is disqualified if any score is below that criterion's gate
Qualified tools rank first, by weighted score; disqualified tools follow.
"""

import argparse
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_CRITERIA = HERE / "criteria.yaml"
MAX_SCORE = 4


def load_yaml(path):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def score_tool(criteria, scores):
    """Return (weighted score 0-100, list of failed gates) for one tool."""
    total_weight = sum(c["weight"] for c in criteria)
    points = 0
    failed = []
    for c in criteria:
        value = scores.get(c["id"])
        if not isinstance(value, int) or not 0 <= value <= MAX_SCORE:
            raise ValueError(f"score for {c['id']} must be an integer 0-4, got {value!r}")
        points += c["weight"] * value
        if value < c.get("gate", 0):
            failed.append(f"{c['name']} ({value} < {c['gate']})")
    return 100 * points / (total_weight * MAX_SCORE), failed


def rank(criteria, tools):
    """Return rows sorted: qualified by score, then disqualified by score."""
    rows = []
    for name, scores in tools.items():
        value, failed = score_tool(criteria, scores)
        rows.append({"tool": name, "score": value, "failed": failed})
    rows.sort(key=lambda r: (bool(r["failed"]), -r["score"], r["tool"]))
    return rows


def weakest(criteria, scores, count=2):
    """Return the names of the heaviest-weighted criteria with the biggest gaps."""
    gaps = sorted(criteria, key=lambda c: -c["weight"] * (MAX_SCORE - scores[c["id"]]))
    return [c["name"] for c in gaps[:count] if scores[c["id"]] < MAX_SCORE]


def render(criteria, data, rows):
    lines = [
        "# Vendor scorecard",
        "",
        f"Evaluated by {data.get('evaluated_by', 'n/a')} on {data.get('date', 'n/a')}.",
        "Scores are synthetic. Tools A-D are not real products.",
        "",
        "| Rank | Tool | Score /100 | Status |",
        "|--:|---|--:|---|",
    ]
    for i, r in enumerate(rows, 1):
        status = "Disqualified" if r["failed"] else "Qualified"
        lines.append(f"| {i} | {r['tool']} | {r['score']:.1f} | {status} |")
    failed_rows = [r for r in rows if r["failed"]]
    if failed_rows:
        lines += ["", "## Failed gates", ""]
        for r in failed_rows:
            lines.append(f"- **{r['tool']}**")
            lines += [f"  - {gate}" for gate in r["failed"]]
    lines += ["", "## Biggest weighted gaps (qualified tools)", ""]
    for r in rows:
        if not r["failed"]:
            gaps = weakest(criteria, data["tools"][r["tool"]])
            lines.append(f"- **{r['tool']}**: " + ("; ".join(gaps) or "none"))
    gated = [c for c in criteria if c.get("gate")]
    lines += ["", "## Must-have gates", "", "| Criterion | Weight | Gate |", "|---|--:|--:|"]
    for c in gated:
        lines.append(f"| {c['name']} | {c['weight']} | {c['gate']} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scores")
    parser.add_argument("--criteria", default=DEFAULT_CRITERIA)
    args = parser.parse_args(argv)
    criteria = load_yaml(args.criteria)["criteria"]
    data = load_yaml(args.scores)
    print(render(criteria, data, rank(criteria, data["tools"])), end="")


if __name__ == "__main__":
    main()
