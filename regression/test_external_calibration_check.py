from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_calibration_check import (
    build_phase2_external_calibration_check,
    render_phase2_external_calibration_check,
    write_phase2_external_calibration_check_json,
    write_phase2_external_calibration_check_report,
)


def test_external_calibration_check_chooses_zudilin_2002_anchor() -> None:
    check = build_phase2_external_calibration_check()

    assert check.chosen_anchor_id == "zudilin_2002_third_order_zeta5_bridge"
    assert "third-order Apéry-like recursion" in check.chosen_source
    assert len(check.calibration_invariants) == 3
    assert any(item.invariant_id == "linear_form_normalization" for item in check.calibration_invariants)
    assert "baseline dual F_7 exact coefficient packet" in check.next_probe_contract


def test_external_calibration_check_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_calibration_check()

    assert "Phase 2 external calibration check" in report
    assert "zudilin_2002_third_order_zeta5_bridge" in report
    assert "Calibration invariants" in report
    assert "parasitic_channel_explicitness" in report

    report_path = write_phase2_external_calibration_check_report(tmp_path / "calibration.md")
    json_path = write_phase2_external_calibration_check_json(tmp_path / "calibration.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["chosen_anchor_id"] == "zudilin_2002_third_order_zeta5_bridge"
    assert payload["calibration_invariants"][1]["invariant_id"] == "parasitic_channel_explicitness"
