from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_bridge_implementation_calibration import (
    build_phase2_external_bridge_implementation_calibration,
    render_phase2_external_bridge_implementation_calibration,
    write_phase2_external_bridge_implementation_calibration_json,
    write_phase2_external_bridge_implementation_calibration_report,
)


def test_external_bridge_implementation_calibration_is_ready_for_comparison_impl() -> None:
    calibration = build_phase2_external_bridge_implementation_calibration()

    assert calibration.calibration_id == "bz_phase2_external_bridge_implementation_calibration"
    assert calibration.bridge_id == "zudilin_2002_third_order_zeta5_bridge"
    assert calibration.readiness_status == "ready_for_bridge_comparison_implementation"
    assert len(calibration.rules) == 3
    assert calibration.rules[0].rule_id == "compare_channel_shape_only"


def test_external_bridge_implementation_calibration_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_bridge_implementation_calibration()

    assert "Phase 2 external bridge implementation calibration" in report
    assert "Accepted asymmetry" in report
    assert "compare_channel_shape_only" in report
    assert "accept_sequence_strength_gap" in report

    report_path = write_phase2_external_bridge_implementation_calibration_report(tmp_path / "calibration.md")
    json_path = write_phase2_external_bridge_implementation_calibration_json(tmp_path / "calibration.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["readiness_status"] == "ready_for_bridge_comparison_implementation"
    assert payload["rules"][2]["rule_id"] == "accept_sequence_strength_gap"
