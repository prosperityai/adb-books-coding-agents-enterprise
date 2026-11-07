# Purpose: tests for pilot/sample_size.py, pilot/make_synthetic.py and pilot/did.py.
# Book: Coding Agents in the Enterprise, Chapter 8
# Licence: MIT (see LICENSE)
import csv

import did
import make_synthetic
import pytest
import sample_size


def test_textbook_sample_size():
    # d = 0.5, alpha 0.05, power 0.8 -> 63 per group (normal approximation).
    assert sample_size.per_group(sd=1.0, effect=0.5) == 63


def test_design_effect_inflates_team_assignment():
    deff, engineers, teams = sample_size.clustered(63, team_size=8, icc=0.1)
    assert deff == pytest.approx(1.7)
    assert teams == 14 and engineers == 112


def test_no_clustering_when_icc_zero():
    assert sample_size.clustered(63, 8, 0.0) == (1.0, 64, 8)


def test_synthetic_data_is_deterministic():
    assert make_synthetic.generate() == make_synthetic.generate()


def test_committed_csv_matches_generator():
    with open(make_synthetic.OUT, encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    fresh = [{k: str(v) for k, v in r.items()} for r in make_synthetic.generate()]
    assert rows == fresh


def test_did_removes_common_trend(tmp_path):
    path = tmp_path / "p.csv"
    lines = ["team,group,period,week,m"]
    for team, group, base, post in [("P1", "pilot", 2, 3), ("P2", "pilot", 3, 4),
                                    ("C1", "comparison", 2, 2.5), ("C2", "comparison", 3, 3.5)]:
        lines += [f"{team},{group},baseline,1,{base}", f"{team},{group},pilot,2,{post}"]
    path.write_text("\n".join(lines) + "\n")
    r = did.did(did.load(path, "m"))
    assert r["effect"] == pytest.approx(0.5)


def test_did_recovers_synthetic_effect():
    data = did.load(make_synthetic.OUT, "prs_per_engineer")
    r = did.did(data)
    low, high = did.bootstrap(data, reps=500)
    assert low < r["effect"] < high
    assert low <= make_synthetic.TRUE_EFFECT <= high + 0.05
