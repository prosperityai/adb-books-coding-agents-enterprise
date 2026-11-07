# Purpose: collect pull-request metrics from GitHub (or an offline JSON file) and split
#          them into agent-authored and human-authored work.
# Book: Coding Agents in the Enterprise, Chapter 10
# Licence: MIT (see LICENSE)
"""GitHub pull-request metrics collector.

Run (offline, synthetic data, no network):
    python3 metrics/collect.py --offline metrics/sample-prs.json \
        --since 2026-07-01 --until 2026-10-01 --out examples/metrics.json

Run (live GitHub REST API; token needs read access to pull requests):
    export GITHUB_TOKEN=...
    python3 metrics/collect.py --repo owner/name --since 2026-07-01 --out metrics.json

Metrics, for PRs merged in [since, until):
    agent share        = agent-authored merged PRs / all merged PRs
    cycle time         = merged_at - created_at, median hours
    time to 1st review = first submitted review - created_at, median hours
    PR size            = additions + deletions, median lines
    rework rate        = share of merged PRs that a fix/revert PR, merged within
                         the window, later corrected (last PR to touch one of the
                         fix's files; an approximation of git blame)
Agent detection rules live in metrics/agent-rules.yaml.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from statistics import median

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_RULES = HERE / "agent-rules.yaml"
API = "https://api.github.com"


def parse_time(value):
    """Parse an ISO 8601 timestamp (GitHub uses ...Z) to an aware datetime."""
    if value is None:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_day(value):
    return dt.datetime.fromisoformat(value).replace(tzinfo=dt.UTC)


def load_rules(path=DEFAULT_RULES):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def agent_reason(pr, rules):
    """Return why a PR counts as agent-authored ('label', 'branch', ...), or None."""
    if set(pr.get("labels", [])) & set(rules.get("agent_labels", [])):
        return "label"
    if any(pr.get("head_ref", "").startswith(p) for p in rules.get("agent_branch_prefixes", [])):
        return "branch"
    if pr.get("author") in rules.get("agent_authors", []):
        return "author"
    pattern = rules.get("agent_trailer_pattern")
    if pattern and any(re.search(pattern, m, re.IGNORECASE) for m in pr.get("commit_messages", [])):
        return "trailer"
    return None


def is_fix(pr, rules):
    if set(pr.get("labels", [])) & set(rules.get("fix_labels", [])):
        return True
    return bool(re.search(rules.get("fix_title_pattern", "^$"), pr["title"], re.IGNORECASE))


def rework_flags(merged_prs, rules):
    """Return {PR number: True/False}: was the PR reworked by a later fix?

    For each fix PR, and each file it touches, blame the most recent earlier
    merged PR that touched that file, if it merged within the window before
    the fix. This is the "last toucher" approximation of git blame.
    """
    window = dt.timedelta(days=rules.get("rework_window_days", 14))
    ordered = sorted(merged_prs, key=lambda p: parse_time(p["merged_at"]))
    flags = {p["number"]: False for p in ordered}
    for i, fix in enumerate(ordered):
        if not is_fix(fix, rules):
            continue
        fixed_at = parse_time(fix["merged_at"])
        for path in fix.get("files", []):
            for earlier in reversed(ordered[:i]):
                if path in earlier.get("files", []):
                    if fixed_at - parse_time(earlier["merged_at"]) <= window:
                        flags[earlier["number"]] = True
                    break
    return flags


def hours(a, b):
    return (parse_time(b) - parse_time(a)).total_seconds() / 3600


def summarise(prs, rework_flags):
    """Medians and rates for one slice of merged PRs."""
    if not prs:
        return {"merged_prs": 0, "cycle_hours": None, "first_review_hours": None,
                "size_lines": None, "rework_rate": None}
    reviewed = [hours(p["created_at"], p["first_review_at"])
                for p in prs if p.get("first_review_at")]
    return {
        "merged_prs": len(prs),
        "cycle_hours": round(median(hours(p["created_at"], p["merged_at"]) for p in prs), 1),
        "first_review_hours": round(median(reviewed), 1) if reviewed else None,
        "size_lines": median(p["additions"] + p["deletions"] for p in prs),
        "rework_rate": round(sum(rework_flags[p["number"]] for p in prs) / len(prs), 3),
    }


def compute(prs, rules, since, until=None):
    """Return the metrics dictionary for PRs merged in [since, until)."""
    merged_all = [p for p in prs if p.get("merged_at")]
    in_window = [p for p in merged_all
                 if parse_time(p["merged_at"]) >= since
                 and (until is None or parse_time(p["merged_at"]) < until)]
    flags = rework_flags(merged_all, rules)
    reasons = {p["number"]: agent_reason(p, rules) for p in in_window}
    agent = [p for p in in_window if reasons[p["number"]]]
    human = [p for p in in_window if not reasons[p["number"]]]
    by_reason = {}
    for r in reasons.values():
        if r:
            by_reason[r] = by_reason.get(r, 0) + 1
    return {
        "since": since.date().isoformat(),
        "until": until.date().isoformat() if until else None,
        "agent_share": round(len(agent) / len(in_window), 3) if in_window else None,
        "agent_detected_by": dict(sorted(by_reason.items())),
        "all": summarise(in_window, flags),
        "agent": summarise(agent, flags),
        "human": summarise(human, flags),
    }


# ---- Live GitHub collection (stdlib urllib) --------------------------------

def get_json(url, token):
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "adb-books-coding-agents-metrics",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_github(repo, since, token, max_file_pages=3):
    """Return normalised PR records for PRs updated since `since`.

    Uses about four API calls per merged PR; mind the rate limit on big repos.
    """
    base = f"{API}/repos/{repo}/pulls"
    records = []
    page = 1
    while True:
        batch = get_json(f"{base}?state=closed&sort=updated&direction=desc"
                         f"&per_page=100&page={page}", token)
        if not batch:
            break
        for pr in batch:
            if not pr.get("merged_at"):
                continue
            n = pr["number"]
            detail = get_json(f"{base}/{n}", token)
            reviews = get_json(f"{base}/{n}/reviews?per_page=100", token)
            commits = get_json(f"{base}/{n}/commits?per_page=100", token)
            files = []
            for fpage in range(1, max_file_pages + 1):
                chunk = get_json(f"{base}/{n}/files?per_page=100&page={fpage}", token)
                files += [f["filename"] for f in chunk]
                if len(chunk) < 100:
                    break
            submitted = sorted(r["submitted_at"] for r in reviews if r.get("submitted_at"))
            records.append({
                "number": n,
                "title": pr["title"],
                "author": pr["user"]["login"],
                "labels": [label["name"] for label in pr["labels"]],
                "head_ref": pr["head"]["ref"],
                "created_at": pr["created_at"],
                "merged_at": pr["merged_at"],
                "first_review_at": submitted[0] if submitted else None,
                "additions": detail["additions"],
                "deletions": detail["deletions"],
                "files": files,
                "commit_messages": [c["commit"]["message"] for c in commits],
            })
        if parse_time(batch[-1]["updated_at"]) < since:
            break
        page += 1
    return records


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--repo", help="owner/name, read live from GitHub")
    source.add_argument("--offline", help="JSON file of normalised PR records")
    p.add_argument("--since", required=True, help="YYYY-MM-DD, first merge day included")
    p.add_argument("--until", help="YYYY-MM-DD, first merge day excluded")
    p.add_argument("--rules", default=DEFAULT_RULES)
    p.add_argument("--out", help="write metrics JSON here (default: stdout)")
    args = p.parse_args(argv)
    since = parse_day(args.since)
    until = parse_day(args.until) if args.until else None
    if args.offline:
        with open(args.offline, encoding="utf-8") as handle:
            prs = json.load(handle)
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("Set GITHUB_TOKEN (read access to pull requests) or use --offline.")
        prs = fetch_github(args.repo, since, token)
    result = compute(prs, load_rules(args.rules), since, until)
    result["source"] = args.repo or Path(args.offline).name
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
