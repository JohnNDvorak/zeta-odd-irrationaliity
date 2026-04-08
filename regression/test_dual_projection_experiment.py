from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.dual_projection_experiment import (
    build_phase2_dual_projection_experiment_plan,
    render_phase2_dual_projection_experiment_plan,
    write_phase2_dual_projection_experiment_plan_json,
    write_phase2_dual_projection_experiment_plan_report,
)


def test_dual_projection_experiment_plan_has_bounded_scope() -> None:
    plan = build_phase2_dual_projection_experiment_plan()

    assert plan.plan_id == "bz_phase2_dual_projection_experiment_plan"
    assert plan.driving_path_id == "baseline_dual_projection_path"
    assert any("n=435" in item for item in plan.non_goals)
    assert any(milestone.milestone_id == "projection_target_spec" for milestone in plan.milestones)
    assert any(milestone.milestone_id == "external_calibration_check" for milestone in plan.milestones)
    assert any("representation rewrite" in item for item in plan.stop_conditions)


def test_dual_projection_experiment_plan_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_dual_projection_experiment_plan()

    assert "Phase 2 dual projection experiment plan" in report
    assert "baseline_dual_projection_path" in report
    assert "projection_target_spec" in report
    assert "external_calibration_check" in report
    assert "bounded projection probe" in report

    report_path = write_phase2_dual_projection_experiment_plan_report(tmp_path / "plan.md")
    json_path = write_phase2_dual_projection_experiment_plan_json(tmp_path / "plan.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["plan_id"] == "bz_phase2_dual_projection_experiment_plan"
    assert payload["milestones"][0]["milestone_id"] == "projection_target_spec"
