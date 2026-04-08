from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_bridge_normalization_note import (
    build_phase2_external_bridge_normalization_note,
    render_phase2_external_bridge_normalization_note,
    write_phase2_external_bridge_normalization_note_json,
    write_phase2_external_bridge_normalization_note_report,
)


def test_external_bridge_normalization_note_accepts_finite_window_asymmetry() -> None:
    note = build_phase2_external_bridge_normalization_note()

    assert note.note_id == "bz_phase2_external_bridge_normalization_note"
    assert note.bridge_id == "zudilin_2002_third_order_zeta5_bridge"
    assert "finite-window exact" in note.accepted_sequence_asymmetry
    assert len(note.channel_comparisons) == 3
    assert note.channel_comparisons[2].channel_id == "sequence_level_object"


def test_external_bridge_normalization_note_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_bridge_normalization_note()

    assert "Phase 2 external bridge normalization note" in report
    assert "Accepted sequence asymmetry" in report
    assert "leading_target_channel" in report
    assert "companion_channel" in report
    assert "sequence_level_object" in report

    report_path = write_phase2_external_bridge_normalization_note_report(tmp_path / "note.md")
    json_path = write_phase2_external_bridge_normalization_note_json(tmp_path / "note.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["bridge_id"] == "zudilin_2002_third_order_zeta5_bridge"
    assert payload["channel_comparisons"][0]["channel_id"] == "leading_target_channel"
