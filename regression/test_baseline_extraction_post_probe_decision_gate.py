from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_extraction_post_probe_decision_gate import (
    build_baseline_extraction_post_probe_decision_gate,
    render_baseline_extraction_post_probe_decision_gate,
    write_baseline_extraction_post_probe_decision_gate_json,
    write_baseline_extraction_post_probe_decision_gate_report,
)


def test_baseline_extraction_post_probe_decision_gate_continues_extraction() -> None:
    gate = build_baseline_extraction_post_probe_decision_gate()

    assert gate.gate_id == "bz_phase2_baseline_extraction_post_probe_decision_gate"
    assert gate.source_probe_id == "bz_phase2_baseline_extraction_probe_v1"
    assert gate.shared_window_end == 80
    assert gate.outcome == "continue_baseline_extraction"
    assert any(item.verdict == "not_yet_satisfied" for item in gate.statuses)


def test_baseline_extraction_post_probe_decision_gate_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_extraction_post_probe_decision_gate()

    assert "Phase 2 baseline extraction post-probe decision gate" in report
    assert "continue_baseline_extraction" in report
    assert "Next step" in report

    report_path = write_baseline_extraction_post_probe_decision_gate_report(tmp_path / "gate.md")
    json_path = write_baseline_extraction_post_probe_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_probe_id"] == "bz_phase2_baseline_extraction_probe_v1"
    assert payload["statuses"][0]["criterion_id"] == "baseline_native_object"
