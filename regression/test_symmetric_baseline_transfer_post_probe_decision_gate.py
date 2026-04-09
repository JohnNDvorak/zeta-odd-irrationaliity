from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_baseline_transfer_post_probe_decision_gate import (
    build_symmetric_baseline_transfer_post_probe_decision_gate,
    render_symmetric_baseline_transfer_post_probe_decision_gate,
    write_symmetric_baseline_transfer_post_probe_decision_gate_json,
    write_symmetric_baseline_transfer_post_probe_decision_gate_report,
)


def test_symmetric_baseline_transfer_post_probe_decision_gate_continues_to_family_probe() -> None:
    gate = build_symmetric_baseline_transfer_post_probe_decision_gate()

    assert gate.gate_id == "bz_phase2_symmetric_baseline_transfer_post_probe_decision_gate"
    assert gate.outcome == "continue_symmetric_baseline_transfer_family_probe"
    assert len(gate.statuses) == 3


def test_symmetric_baseline_transfer_post_probe_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_baseline_transfer_post_probe_decision_gate()

    assert "Phase 2 symmetric-to-baseline transfer post-probe decision gate" in report
    assert "continue_symmetric_baseline_transfer_family_probe" in report

    report_path = write_symmetric_baseline_transfer_post_probe_decision_gate_report(tmp_path / "gate.md")
    json_path = write_symmetric_baseline_transfer_post_probe_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["outcome"] == "continue_symmetric_baseline_transfer_family_probe"
