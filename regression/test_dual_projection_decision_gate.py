from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.dual_projection_decision_gate import (
    build_phase2_dual_projection_decision_gate,
    render_phase2_dual_projection_decision_gate,
    write_phase2_dual_projection_decision_gate_json,
    write_phase2_dual_projection_decision_gate_report,
)


def test_dual_projection_decision_gate_prefers_external_bridge_path() -> None:
    gate = build_phase2_dual_projection_decision_gate()

    assert gate.gate_id == "bz_phase2_dual_projection_decision_gate"
    assert gate.outcome == "switch_to_external_bridge_calibration"
    assert any("bookkeeping-only" in item for item in gate.evidence)
    assert any("n=435" in item for item in gate.rejected_next_steps)
    assert "Zudilin 2002" in gate.next_main_line or "Zudilin 2018" in gate.next_main_line


def test_dual_projection_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_dual_projection_decision_gate()

    assert "Phase 2 dual projection decision gate" in report
    assert "switch_to_external_bridge_calibration" in report
    assert "Rejected next steps" in report
    assert "Next main line" in report

    report_path = write_phase2_dual_projection_decision_gate_report(tmp_path / "gate.md")
    json_path = write_phase2_dual_projection_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["outcome"] == "switch_to_external_bridge_calibration"
