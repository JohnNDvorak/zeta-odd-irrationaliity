from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_coupled_channel_comparison_probe import (
    build_zudilin_2002_coupled_channel_comparison_probe,
    render_zudilin_2002_coupled_channel_comparison_probe,
    write_zudilin_2002_coupled_channel_comparison_probe_json,
    write_zudilin_2002_coupled_channel_comparison_probe_report,
)


def test_zudilin_2002_coupled_channel_comparison_probe_hashes_ordered_pairs() -> None:
    probe = build_zudilin_2002_coupled_channel_comparison_probe(max_n=7)

    assert probe.probe_id == "bz_phase2_zudilin_2002_coupled_channel_comparison_probe"
    assert probe.shared_window_end == 7
    assert probe.verdict == "coupled_comparison_ready_but_not_equivalent"
    assert len(probe.baseline_pair_hash) == 64
    assert len(probe.bridge_pair_hash) == 64


def test_zudilin_2002_coupled_channel_comparison_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_coupled_channel_comparison_probe(max_n=7)

    assert "Phase 2 Zudilin 2002 coupled-channel comparison probe" in report
    assert "coupled_comparison_ready_but_not_equivalent" in report
    assert "Sample paired data" in report

    report_path = write_zudilin_2002_coupled_channel_comparison_probe_report(
        max_n=7, output_path=tmp_path / "probe.md"
    )
    json_path = write_zudilin_2002_coupled_channel_comparison_probe_json(
        max_n=7, output_path=tmp_path / "probe.json"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["samples"][0]["n"] == 1
