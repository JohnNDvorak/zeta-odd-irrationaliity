from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_extraction_implementation_plan import (
    build_baseline_extraction_implementation_plan,
    render_baseline_extraction_implementation_plan,
    write_baseline_extraction_implementation_plan_json,
    write_baseline_extraction_implementation_plan_report,
)


def test_baseline_extraction_implementation_plan_uses_bridge_as_calibration_only() -> None:
    plan = build_baseline_extraction_implementation_plan()

    assert plan.plan_id == "bz_phase2_baseline_extraction_implementation_plan"
    assert plan.target_object == "baseline_dual_f7_exact_coefficient_packet"
    assert len(plan.milestones) == 4
    assert "calibration" in plan.bridge_role
    assert "baseline_pair_object_spec" in plan.next_step


def test_baseline_extraction_implementation_plan_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_extraction_implementation_plan()

    assert "Phase 2 baseline extraction implementation plan" in report
    assert "Bridge role" in report
    assert "Milestones" in report

    report_path = write_baseline_extraction_implementation_plan_report(tmp_path / "plan.md")
    json_path = write_baseline_extraction_implementation_plan_json(tmp_path / "plan.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["target_object"] == "baseline_dual_f7_exact_coefficient_packet"
    assert payload["milestones"][0]["milestone_id"] == "baseline_pair_object_spec"
