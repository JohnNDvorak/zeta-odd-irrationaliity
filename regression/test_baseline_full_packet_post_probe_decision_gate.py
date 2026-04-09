from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_full_packet_post_probe_decision_gate import (
    build_baseline_full_packet_post_probe_decision_gate,
    render_baseline_full_packet_post_probe_decision_gate,
    write_baseline_full_packet_post_probe_decision_gate_json,
    write_baseline_full_packet_post_probe_decision_gate_report,
)


def test_baseline_full_packet_post_probe_decision_gate_continues_compression() -> None:
    gate = build_baseline_full_packet_post_probe_decision_gate()

    assert gate.gate_id == "bz_phase2_baseline_full_packet_post_probe_decision_gate"
    assert gate.outcome == "continue_full_packet_compression"
    assert gate.statuses[2].criterion_id == "pairwise_neutrality"
    assert gate.statuses[3].verdict == "not_yet_satisfied"


def test_baseline_full_packet_post_probe_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_full_packet_post_probe_decision_gate()

    assert "Phase 2 baseline full-packet post-probe decision gate" in report
    assert "pairwise_neutrality" in report

    report_path = write_baseline_full_packet_post_probe_decision_gate_report(tmp_path / "gate.md")
    json_path = write_baseline_full_packet_post_probe_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["outcome"] == "continue_full_packet_compression"
