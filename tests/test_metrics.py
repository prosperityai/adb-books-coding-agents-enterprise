# Purpose: tests for metrics/collect.py (agent detection, rework, medians) and report.py.
# Book: Coding Agents in the Enterprise, Chapter 10
# Licence: MIT (see LICENSE)
import json

import collect
import make_sample
import report

RULES = collect.load_rules()
SINCE = collect.parse_day("2026-07-01")


def pr(number, merged, files=("a.py",), title="Add thing", **extra):
    base = {"number": number, "title": title, "author": "dev01", "labels": [],
            "head_ref": "feature/x", "created_at": "2026-07-01T00:00:00Z",
            "merged_at": merged, "first_review_at": "2026-07-01T02:00:00Z",
            "additions": 10, "deletions": 5, "files": list(files), "commit_messages": []}
    base.update(extra)
    return base


def test_agent_detection_rules():
    assert collect.agent_reason(pr(1, "x", labels=["agent-authored"]), RULES) == "label"
    assert collect.agent_reason(pr(1, "x", head_ref="claude/fix-1"), RULES) == "branch"
    assert collect.agent_reason(pr(1, "x", author="example-agent[bot]"), RULES) == "author"
    msg = ["Do it\n\nCo-Authored-By: Claude <noreply@example.com>"]
    assert collect.agent_reason(pr(1, "x", commit_messages=msg), RULES) == "trailer"
    assert collect.agent_reason(pr(1, "x"), RULES) is None


def test_rework_blames_last_toucher_within_window():
    prs = [pr(1, "2026-07-02T00:00:00Z"),
           pr(2, "2026-07-05T00:00:00Z"),
           pr(3, "2026-07-08T00:00:00Z", title="Fix crash", files=["a.py"]),
           pr(4, "2026-07-02T00:00:00Z", files=["b.py"]),
           pr(5, "2026-08-30T00:00:00Z", title="Hotfix", files=["b.py"])]
    flags = collect.rework_flags(prs, RULES)
    assert flags[2] is True        # last PR to touch a.py before the fix
    assert flags[1] is False       # an older toucher is not blamed
    assert flags[4] is False       # fix came after the 14-day window


def test_compute_splits_agent_and_human():
    prs = [pr(1, "2026-07-01T10:00:00Z", head_ref="codex/a"),
           pr(2, "2026-07-01T20:00:00Z"),
           pr(3, "2026-06-20T00:00:00Z")]        # merged before the window
    m = collect.compute(prs, RULES, SINCE)
    assert m["all"]["merged_prs"] == 2
    assert m["agent_share"] == 0.5
    assert m["agent"]["cycle_hours"] == 10.0
    assert m["human"]["first_review_hours"] == 2.0
    assert m["all"]["size_lines"] == 15


def test_offline_sample_matches_generator():
    with open(make_sample.OUT, encoding="utf-8") as handle:
        assert json.load(handle) == make_sample.generate()


def test_offline_cli_and_report(tmp_path):
    out = tmp_path / "m.json"
    collect.main(["--offline", str(make_sample.OUT), "--since", "2026-07-01",
                  "--until", "2026-10-01", "--out", str(out)])
    m = json.loads(out.read_text())
    assert 0 < m["agent_share"] < 1
    text = report.render(m, "2026-Q3", cost_per_month=3000)
    assert "Quarterly scorecard: 2026-Q3" in text
    assert "Cost per merged PR" in text
    assert "## Do not target" in text
