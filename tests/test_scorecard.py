# Purpose: tests for scorecard/score.py (weighting, gates, ranking order).
# Book: Coding Agents in the Enterprise, Chapter 3
# Licence: MIT (see LICENSE)
import pytest
import score

CRITERIA = [
    {"id": "a", "name": "A", "weight": 60, "gate": 3},
    {"id": "b", "name": "B", "weight": 40},
]


def test_weighted_score_is_out_of_100():
    value, failed = score.score_tool(CRITERIA, {"a": 4, "b": 4})
    assert value == 100 and failed == []
    value, _ = score.score_tool(CRITERIA, {"a": 3, "b": 1})
    assert value == pytest.approx(100 * (60 * 3 + 40 * 1) / 400)


def test_gate_disqualifies_even_a_high_scorer():
    rows = score.rank(CRITERIA, {"X": {"a": 2, "b": 4}, "Y": {"a": 3, "b": 0}})
    assert [r["tool"] for r in rows] == ["Y", "X"]
    assert rows[1]["failed"] == ["A (2 < 3)"]


def test_bad_score_rejected():
    with pytest.raises(ValueError):
        score.score_tool(CRITERIA, {"a": 5, "b": 1})


def test_example_ranking():
    criteria = score.load_yaml(score.DEFAULT_CRITERIA)["criteria"]
    assert sum(c["weight"] for c in criteria) == 100
    data = score.load_yaml(score.HERE / "example-scores.yaml")
    rows = score.rank(criteria, data["tools"])
    assert rows[0]["tool"] == "Tool B"
    assert rows[-1]["tool"] == "Tool C" and rows[-1]["failed"]
