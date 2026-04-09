from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_bridge_comparison_probe import (
    build_zudilin_2002_bridge_comparison_probe,
    render_zudilin_2002_bridge_comparison_probe,
    write_zudilin_2002_bridge_comparison_probe_json,
    write_zudilin_2002_bridge_comparison_probe_report,
)


def test_zudilin_2002_bridge_comparison_probe_compares_real_objects() -> None:
    probe = build_zudilin_2002_bridge_comparison_probe(max_n=7)

    assert probe.probe_id == "bz_phase2_zudilin_2002_bridge_comparison_probe"
    assert probe.shared_window_end == 7
    assert len(probe.channel_comparisons) == 2
    assert probe.channel_comparisons[0].verdict == "comparison_ready_but_not_equivalent"
    assert len(probe.channel_comparisons[0].baseline_window_hash) == 64
    assert len(probe.channel_comparisons[0].bridge_window_hash) == 64


def test_zudilin_2002_bridge_comparison_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_bridge_comparison_probe(max_n=7)

    assert "Phase 2 Zudilin 2002 bridge comparison probe" in report
    assert "comparison_ready_but_not_equivalent" in report
    assert "Overall verdict" in report

    report_path = write_zudilin_2002_bridge_comparison_probe_report(max_n=7, output_path=tmp_path / "cmp.md")
    json_path = write_zudilin_2002_bridge_comparison_probe_json(max_n=7, output_path=tmp_path / "cmp.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["channel_comparisons"][1]["channel_id"] == "companion_channel"
