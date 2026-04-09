from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_coupled_channel_comparison_target import (
    build_zudilin_2002_coupled_channel_comparison_target,
    render_zudilin_2002_coupled_channel_comparison_target,
    write_zudilin_2002_coupled_channel_comparison_target_json,
    write_zudilin_2002_coupled_channel_comparison_target_report,
)


def test_zudilin_2002_coupled_channel_comparison_target_builds_ordered_pair_object() -> None:
    target = build_zudilin_2002_coupled_channel_comparison_target(max_n=7)

    assert target.target_id == "bz_phase2_zudilin_2002_coupled_channel_comparison_target"
    assert target.shared_window_end == 7
    assert len(target.fields) == 3
    assert target.fields[0].status == "ready_for_hash_probe"


def test_zudilin_2002_coupled_channel_comparison_target_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_coupled_channel_comparison_target(max_n=7)

    assert "Phase 2 Zudilin 2002 coupled-channel comparison target" in report
    assert "ordered pair" in report
    assert "Recommendation" in report

    report_path = write_zudilin_2002_coupled_channel_comparison_target_report(
        max_n=7, output_path=tmp_path / "target.md"
    )
    json_path = write_zudilin_2002_coupled_channel_comparison_target_json(
        max_n=7, output_path=tmp_path / "target.json"
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["fields"][2]["field_id"] == "sequence_strength_disclaimer"
