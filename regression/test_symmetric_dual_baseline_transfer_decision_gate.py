from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_transfer_decision_gate import (
    build_symmetric_dual_baseline_transfer_decision_gate,
    render_symmetric_dual_baseline_transfer_decision_gate,
    write_symmetric_dual_baseline_transfer_decision_gate_json,
    write_symmetric_dual_baseline_transfer_decision_gate_report,
)


def test_symmetric_dual_baseline_transfer_decision_gate_hits_hard_wall() -> None:
    gate = build_symmetric_dual_baseline_transfer_decision_gate()

    assert gate.gate_id == "bz_phase2_symmetric_dual_baseline_transfer_decision_gate"
    assert gate.outcome == "hard_wall_symmetric_dual_baseline_low_complexity_transfer_exhausted"
    assert gate.pivot_options == (
        "richer_dual_packet_transfer_family",
        "different_transfer_object",
    )
    assert len(gate.statuses) == 3


def test_symmetric_dual_baseline_transfer_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_dual_baseline_transfer_decision_gate()

    assert "Phase 2 symmetric-dual to baseline-dual transfer decision gate" in report
    assert "different_transfer_object" in report

    report_path = write_symmetric_dual_baseline_transfer_decision_gate_report(tmp_path / "gate.md")
    json_path = write_symmetric_dual_baseline_transfer_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["outcome"] == "hard_wall_symmetric_dual_baseline_low_complexity_transfer_exhausted"
