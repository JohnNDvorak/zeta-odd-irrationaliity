from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_coupled_map_decision_gate import (
    build_zudilin_2002_coupled_map_decision_gate,
    render_zudilin_2002_coupled_map_decision_gate,
    write_zudilin_2002_coupled_map_decision_gate_json,
    write_zudilin_2002_coupled_map_decision_gate_report,
)


def test_zudilin_2002_coupled_map_decision_gate_closes_constant_form_layer() -> None:
    gate = build_zudilin_2002_coupled_map_decision_gate(max_n=7)

    assert gate.gate_id == "bz_phase2_zudilin_2002_coupled_map_decision_gate"
    assert gate.shared_window_end == 7
    assert len(gate.statuses) == 2
    assert all(item.verdict == "closed" for item in gate.statuses)
    assert "constant-form ansatz layer is now closed" in gate.overall_verdict


def test_zudilin_2002_coupled_map_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_coupled_map_decision_gate(max_n=7)

    assert "Phase 2 Zudilin 2002 coupled-map decision gate" in report
    assert "one_channel_polynomial_maps" in report
    assert "constant_coupled_linear_map" in report

    report_path = write_zudilin_2002_coupled_map_decision_gate_report(
        max_n=7, output_path=tmp_path / "gate.md"
    )
    json_path = write_zudilin_2002_coupled_map_decision_gate_json(
        max_n=7, output_path=tmp_path / "gate.json"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["statuses"][0]["layer_id"] == "one_channel_polynomial_maps"
