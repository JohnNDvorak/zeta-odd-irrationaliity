from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_full_packet_compression_decision_gate import (
    build_baseline_full_packet_compression_decision_gate,
    render_baseline_full_packet_compression_decision_gate,
    write_baseline_full_packet_compression_decision_gate_json,
    write_baseline_full_packet_compression_decision_gate_report,
)


def test_baseline_full_packet_compression_decision_gate_hits_hard_wall() -> None:
    gate = build_baseline_full_packet_compression_decision_gate()

    assert gate.gate_id == "bz_phase2_baseline_full_packet_compression_decision_gate"
    assert gate.outcome == "hard_wall_full_packet_pairwise_compression_exhausted"
    assert gate.pivot_options == (
        "richer_full_packet_projection_family",
        "different_baseline_family_source",
    )
    assert len(gate.statuses) == 3


def test_baseline_full_packet_compression_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_full_packet_compression_decision_gate()

    assert "Phase 2 baseline full-packet compression decision gate" in report
    assert "different_baseline_family_source" in report

    report_path = write_baseline_full_packet_compression_decision_gate_report(tmp_path / "gate.md")
    json_path = write_baseline_full_packet_compression_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["outcome"] == "hard_wall_full_packet_pairwise_compression_exhausted"
