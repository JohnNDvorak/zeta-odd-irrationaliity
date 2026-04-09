from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_odd_extraction_rule import (
    build_baseline_odd_extraction_rule,
    render_baseline_odd_extraction_rule,
    write_baseline_odd_extraction_rule_json,
    write_baseline_odd_extraction_rule_report,
)


def test_baseline_odd_extraction_rule_keeps_odd_pair_and_constant_residual_separate() -> None:
    rule = build_baseline_odd_extraction_rule()

    assert rule.rule_id == "bz_phase2_baseline_odd_extraction_rule_v1"
    assert rule.source_spec_id == "bz_phase2_baseline_odd_pair_object_spec"
    assert rule.shared_window_end == 80
    assert len(rule.retained_output_hash) == 64
    assert len(rule.unresolved_residual_hash) == 64
    assert "constant residual" in rule.unresolved_structure[2]


def test_baseline_odd_extraction_rule_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_odd_extraction_rule()

    assert "Phase 2 baseline odd extraction rule" in report
    assert "Confirmed output" in report
    assert "retained zeta(5)" in report

    report_path = write_baseline_odd_extraction_rule_report(tmp_path / "rule.md")
    json_path = write_baseline_odd_extraction_rule_json(tmp_path / "rule.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_spec_id"] == "bz_phase2_baseline_odd_pair_object_spec"
    assert payload["samples"][0]["n"] == 1
