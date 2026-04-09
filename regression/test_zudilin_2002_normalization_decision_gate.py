from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_normalization_decision_gate import (
    build_zudilin_2002_normalization_decision_gate,
    render_zudilin_2002_normalization_decision_gate,
    write_zudilin_2002_normalization_decision_gate_json,
    write_zudilin_2002_normalization_decision_gate_report,
)


def test_zudilin_2002_normalization_decision_gate_stops_polynomial_rescaling_line() -> None:
    gate = build_zudilin_2002_normalization_decision_gate(max_n=7)

    assert gate.gate_id == "bz_phase2_zudilin_2002_normalization_decision_gate"
    assert gate.shared_window_end == 7
    assert len(gate.family_statuses) == 3
    assert all(item.verdict.endswith("_fails") for item in gate.family_statuses)
    assert "stop the polynomial-rescaling subline" in gate.overall_verdict


def test_zudilin_2002_normalization_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_normalization_decision_gate(max_n=7)

    assert "Phase 2 Zudilin 2002 normalization decision gate" in report
    assert "scalar" in report
    assert "quadratic_in_n" in report
    assert "Recommendation" in report

    report_path = write_zudilin_2002_normalization_decision_gate_report(
        max_n=7, output_path=tmp_path / "gate.md"
    )
    json_path = write_zudilin_2002_normalization_decision_gate_json(max_n=7, output_path=tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["family_statuses"][0]["family_id"] == "scalar"
