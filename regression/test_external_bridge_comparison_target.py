from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_bridge_comparison_target import (
    build_phase2_external_bridge_comparison_target,
    render_phase2_external_bridge_comparison_target,
    write_phase2_external_bridge_comparison_target_json,
    write_phase2_external_bridge_comparison_target_report,
)


def test_external_bridge_comparison_target_tracks_three_fields() -> None:
    target = build_phase2_external_bridge_comparison_target()

    assert target.target_id == "bz_phase2_external_bridge_comparison_target"
    assert target.bridge_id == "zudilin_2002_third_order_zeta5_bridge"
    assert target.comparison_mode == "shape_and_reproducibility_before_recurrence"
    assert [field.field_id for field in target.comparison_fields] == [
        "leading_target_channel",
        "companion_channel",
        "sequence_level_object",
    ]
    assert target.comparison_fields[0].current_status == "partially_aligned"
    assert target.comparison_fields[2].current_status == "not_yet_aligned"


def test_external_bridge_comparison_target_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_bridge_comparison_target()

    assert "Phase 2 external bridge comparison target" in report
    assert "leading_target_channel" in report
    assert "companion_channel" in report
    assert "sequence_level_object" in report
    assert "ready_for_comparison_probe" in report

    report_path = write_phase2_external_bridge_comparison_target_report(tmp_path / "comparison.md")
    json_path = write_phase2_external_bridge_comparison_target_json(tmp_path / "comparison.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["overall_status"] == "ready_for_comparison_probe"
    assert payload["comparison_fields"][1]["field_id"] == "companion_channel"
