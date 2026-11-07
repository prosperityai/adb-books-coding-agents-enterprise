# Purpose: generate metrics/sample-prs.json, a synthetic quarter of pull requests for a
#          fictional repository, so collect.py runs without network access. Seeded.
# Book: Coding Agents in the Enterprise, Chapter 10
# Licence: MIT (see LICENSE)
"""Write metrics/sample-prs.json (invented data, fictional repo and people).

Run:
    python3 metrics/make_sample.py
"""

import datetime as dt
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "sample-prs.json"
SEED = 43
START = dt.datetime(2026, 6, 24, 9, tzinfo=dt.UTC)   # a week before Q3, for rework look-back
DAYS = 100
AREAS = ("payments", "ledger", "auth", "api", "reports", "cards", "fx", "kyc")
NAMES = ("models", "service", "routes", "validators", "utils", "jobs")
FILES = [f"src/{area}/{name}.py" for area in AREAS for name in NAMES]
HUMANS = [f"dev{i:02d}" for i in range(1, 19)]


def stamp(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def make_pr(rng, number, created):
    agent = rng.random() < 0.38
    style = rng.choice(["branch", "branch", "trailer", "label", "author"]) if agent else None
    author = "example-agent[bot]" if style == "author" else rng.choice(HUMANS)
    branch = (rng.choice(["claude/", "copilot/", "codex/"]) if style == "branch"
              else rng.choice(["feature/", "chore/", "fix/"])) + f"task-{number}"
    messages = [f"Change for task {number}"]
    if style == "trailer":
        messages.append(f"Refactor task {number}\n\nCo-Authored-By: Claude <noreply@example.com>")
    labels = ["agent-authored"] if style == "label" else []
    size = int(rng.lognormvariate(5.2 if agent else 4.6, 0.7))
    review_wait = rng.lognormvariate(2.0 if agent else 1.5, 0.6)
    cycle = review_wait + rng.lognormvariate(2.6 if agent else 2.5, 0.5)
    return {
        "number": number,
        "title": f"{'Add' if rng.random() < 0.5 else 'Update'} {rng.choice(FILES).split('/')[1]} "
                 f"logic (task {number})",
        "author": author,
        "labels": labels,
        "head_ref": branch,
        "created_at": stamp(created),
        "merged_at": stamp(created + dt.timedelta(hours=cycle)),
        "first_review_at": stamp(created + dt.timedelta(hours=review_wait)),
        "additions": int(size * 0.7),
        "deletions": size - int(size * 0.7),
        "files": rng.sample(FILES, rng.randint(1, 5 if agent else 3)),
        "commit_messages": messages,
        "_agent": agent,
    }


def generate(seed=SEED):
    rng = random.Random(seed)
    prs = []
    number = 1000
    for day in range(DAYS):
        for _ in range(rng.randint(0, 3)):
            number += 1
            created = START + dt.timedelta(days=day, hours=rng.randint(0, 8))
            prs.append(make_pr(rng, number, created))
    # Follow-up fixes: agent PRs are reworked a little more often in this invented data.
    fixes = []
    for pr in prs:
        if rng.random() < (0.10 if pr["_agent"] else 0.05):
            number += 1
            created = dt.datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
            created += dt.timedelta(days=rng.randint(1, 10))
            fixes.append({
                "number": number,
                "title": f"Fix regression from #{pr['number']}",
                "author": rng.choice(HUMANS),
                "labels": ["bug"],
                "head_ref": f"fix/regression-{pr['number']}",
                "created_at": stamp(created),
                "merged_at": stamp(created + dt.timedelta(hours=rng.uniform(2, 20))),
                "first_review_at": stamp(created + dt.timedelta(hours=rng.uniform(0.5, 3))),
                "additions": rng.randint(5, 60),
                "deletions": rng.randint(2, 30),
                "files": [pr["files"][0]],
                "commit_messages": [f"Fix regression from #{pr['number']}"],
                "_agent": False,
            })
    records = prs + fixes
    for r in records:
        del r["_agent"]
    return sorted(records, key=lambda r: r["number"])


if __name__ == "__main__":
    OUT.write_text(json.dumps(generate(), indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}")
