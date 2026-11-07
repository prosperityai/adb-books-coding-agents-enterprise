# Purpose: monthly and annual cost of a coding-agent rollout (seats + metered usage +
#          platform + enablement), cost per engineer, cost per merged PR and the
#          break-even point in engineer-hours, printed as Markdown.
# Book: Coding Agents in the Enterprise, Chapter 2
# Licence: MIT (see LICENSE)
"""Coding-agent cost model.

Run:
    python3 cost/cost_model.py cost/example-bank.yaml

How the maths works (all money is USD per month unless stated):
    average usage   = sum(tier share x tier usage per user)
    metered usage   = seats x average usage
    overage         = max(0, metered usage - seats x included usage per seat)
    tool cost       = seats x seat price + overage
    total           = tool costs + platform + enablement
    merged PRs      = engineers x baseline PRs x (1 + assumed uplift)
    extra PRs       = engineers x baseline PRs x assumed uplift
    break-even hours = total / loaded cost per engineer-hour

Included usage is treated as pooled across seats (as Copilot AI Credits are).
"""

import argparse
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_INPUTS = HERE / "example-bank.yaml"
TIERS = ("light", "regular", "heavy")


def load_inputs(path=DEFAULT_INPUTS):
    """Read the YAML inputs and check tier shares add to 1."""
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    total_share = sum(data["tiers"][t] for t in TIERS)
    if abs(total_share - 1.0) > 1e-9:
        raise ValueError(f"tier shares must add to 1.0, got {total_share}")
    return data


def tool_cost(tool, tiers):
    """Return seat, usage and total cost per month for one tool."""
    seats = tool["seats"]
    avg_usage = sum(tiers[t] * tool["usage_per_user"][t] for t in TIERS)
    metered = seats * avg_usage
    included = seats * tool.get("included_usage_per_seat", 0)
    overage = max(0.0, metered - included)
    seat_cost = seats * tool["seat_price"]
    return {
        "name": tool["name"],
        "seats": seats,
        "seat_cost": seat_cost,
        "avg_usage": avg_usage,
        "metered": metered,
        "overage": overage,
        "total": seat_cost + overage,
    }


def compute(data):
    """Return every figure the report prints."""
    org = data["organisation"]
    tools = [tool_cost(t, data["tiers"]) for t in data["tools"]]
    tools_total = sum(t["total"] for t in tools)
    platform = sum(data.get("platform", {}).values())
    enablement = sum(data.get("enablement", {}).values())
    monthly = tools_total + platform + enablement
    engineers = org["engineers"]
    baseline_prs = engineers * org["baseline_merged_prs_per_engineer_month"]
    uplift = org["assumed_pr_uplift"]
    merged_prs = baseline_prs * (1 + uplift)
    extra_prs = baseline_prs * uplift
    hourly = org["loaded_cost_per_engineer_hour"]
    breakeven_hours = monthly / hourly
    return {
        "tools": tools,
        "tools_total": tools_total,
        "platform": platform,
        "enablement": enablement,
        "monthly": monthly,
        "annual": monthly * 12,
        "per_engineer": monthly / engineers,
        "merged_prs": merged_prs,
        "per_merged_pr": monthly / merged_prs,
        "per_extra_pr": monthly / extra_prs if extra_prs else float("inf"),
        "breakeven_hours": breakeven_hours,
        "breakeven_hours_per_engineer": breakeven_hours / engineers,
    }


def money(value):
    return f"${value:,.0f}"


def render(data, result):
    """Return the Markdown report."""
    org = data["organisation"]
    lines = [
        f"# Cost model: {org['name']} ({org['engineers']} engineers)",
        "",
        "All prices are assumptions as of Nov 2026. Verify before use.",
        "",
        "## Tools (per month)",
        "",
        "| Tool | Seats | Seat cost | Total |",
        "|---|--:|--:|--:|",
    ]
    for t in result["tools"]:
        lines.append(f"| {t['name']} | {t['seats']} | {money(t['seat_cost'])} "
                     f"| {money(t['total'])} |")
    lines += [
        "",
        "Total = seat cost + usage above the included allowance.",
        "",
        "| Tool | Avg usage/user | Metered | Overage |",
        "|---|--:|--:|--:|",
    ]
    for t in result["tools"]:
        lines.append(f"| {t['name']} | {money(t['avg_usage'])} | {money(t['metered'])} "
                     f"| {money(t['overage'])} |")
    lines += ["", "## Monthly total", "", "| Item | Per month |", "|---|--:|",
              f"| Tools | {money(result['tools_total'])} |"]
    for section in ("platform", "enablement"):
        for name, value in data.get(section, {}).items():
            lines.append(f"| {name} | {money(value)} |")
    lines += [
        f"| **Total** | **{money(result['monthly'])}** |",
        "",
        "## Headline figures",
        "",
        "| Measure | Value |",
        "|---|--:|",
        f"| Monthly total | {money(result['monthly'])} |",
        f"| Annual total | {money(result['annual'])} |",
        f"| Cost per engineer per month | {money(result['per_engineer'])} |",
        f"| Merged PRs per month (assumed) | {result['merged_prs']:,.0f} |",
        f"| Cost per merged PR | ${result['per_merged_pr']:,.2f} |",
        f"| Cost per extra PR from uplift | ${result['per_extra_pr']:,.2f} |",
        f"| Break-even, engineer-hours/month | {result['breakeven_hours']:,.0f} |",
        f"| Break-even, hours/engineer/month | {result['breakeven_hours_per_engineer']:.1f} |",
        "",
        f"Uplift assumed: {org['assumed_pr_uplift']:.0%} more merged PRs on a "
        f"baseline of {org['baseline_merged_prs_per_engineer_month']} per engineer "
        "per month.",
        f"Break-even uses a loaded cost of ${org['loaded_cost_per_engineer_hour']} "
        "per engineer-hour.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inputs", nargs="?", default=DEFAULT_INPUTS)
    args = parser.parse_args(argv)
    data = load_inputs(args.inputs)
    print(render(data, compute(data)), end="")


if __name__ == "__main__":
    main()
