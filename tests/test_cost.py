# Purpose: tests for cost/cost_model.py (overage, totals, per-PR and break-even maths).
# Book: Coding Agents in the Enterprise, Chapter 2
# Licence: MIT (see LICENSE)
import copy

import cost_model as cm
import pytest

TIERS = {"light": 0.5, "regular": 0.5, "heavy": 0.0}


def test_included_usage_absorbs_metered_usage():
    tool = {"name": "T", "seats": 10, "seat_price": 39, "included_usage_per_seat": 39,
            "usage_per_user": {"light": 10, "regular": 50, "heavy": 0}}
    r = cm.tool_cost(tool, TIERS)
    assert r["avg_usage"] == 30
    assert r["overage"] == 0
    assert r["total"] == 390


def test_usage_above_allowance_is_billed():
    tool = {"name": "T", "seats": 10, "seat_price": 20, "included_usage_per_seat": 0,
            "usage_per_user": {"light": 100, "regular": 200, "heavy": 0}}
    r = cm.tool_cost(tool, TIERS)
    assert r["overage"] == 1500
    assert r["total"] == 1700


def test_example_bank_headline_figures():
    result = cm.compute(cm.load_inputs())
    assert result["monthly"] == pytest.approx(81900)
    assert result["annual"] == pytest.approx(81900 * 12)
    assert result["per_engineer"] == pytest.approx(204.75)
    assert result["merged_prs"] == pytest.approx(4600)
    assert result["per_merged_pr"] == pytest.approx(81900 / 4600)
    assert result["breakeven_hours"] == pytest.approx(81900 / 95)


def test_tier_shares_must_add_to_one(tmp_path):
    data = copy.deepcopy(cm.load_inputs())
    data["tiers"]["heavy"] = 0.5
    path = tmp_path / "bad.yaml"
    import yaml
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        cm.load_inputs(path)


def test_report_is_narrow():
    data = cm.load_inputs()
    text = cm.render(data, cm.compute(data))
    assert "$81,900" in text
    for line in text.splitlines():
        if line.startswith("|"):
            assert line.count("|") <= 5          # at most 4 columns
