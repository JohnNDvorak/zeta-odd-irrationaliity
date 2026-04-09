from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_odd_extraction_probe import (
    build_baseline_odd_extraction_probe,
    render_baseline_odd_extraction_probe,
    write_baseline_odd_extraction_probe_json,
    write_baseline_odd_extraction_probe_report,
)


def test_baseline_odd_extraction_probe_establishes_odd_pair_summary() -> None:
    probe = build_baseline_odd_extraction_probe()

    assert probe.probe_id == "bz_phase2_baseline_odd_extraction_probe_v1"
    assert probe.source_rule_id == "bz_phase2_baseline_odd_extraction_rule_v1"
    assert probe.shared_window_end == 80
    assert probe.verdict == "baseline_odd_pair_summary_established"
    assert "constant residual" in probe.unresolved_findings[2]


def test_baseline_odd_extraction_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_odd_extraction_probe()

    assert "Phase 2 baseline odd extraction probe" in report
    assert "Stabilized findings" in report
    assert "unresolved constant" in report

    report_path = write_baseline_odd_extraction_probe_report(tmp_path / "probe.md")
    json_path = write_baseline_odd_extraction_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_rule_id"] == "bz_phase2_baseline_odd_extraction_rule_v1"
