from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_bridge_comparison_implementation_note import (
    build_phase2_external_bridge_comparison_implementation_note,
    render_phase2_external_bridge_comparison_implementation_note,
    write_phase2_external_bridge_comparison_implementation_note_json,
    write_phase2_external_bridge_comparison_implementation_note_report,
)


def test_external_bridge_comparison_implementation_note_sets_allowed_and_forbidden_claims() -> None:
    note = build_phase2_external_bridge_comparison_implementation_note()

    assert note.note_id == "bz_phase2_external_bridge_comparison_implementation_note"
    assert note.bridge_id == "zudilin_2002_third_order_zeta5_bridge"
    assert len(note.items) == 3
    assert note.items[0].item_id == "leading_target_channel"
    assert "Do not state or imply" in note.items[0].forbidden_statement


def test_external_bridge_comparison_implementation_note_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_bridge_comparison_implementation_note()

    assert "Phase 2 external bridge comparison implementation note" in report
    assert "Accepted asymmetry" in report
    assert "leading_target_channel" in report
    assert "Forbidden statement" in report

    report_path = write_phase2_external_bridge_comparison_implementation_note_report(tmp_path / "impl.md")
    json_path = write_phase2_external_bridge_comparison_implementation_note_json(tmp_path / "impl.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["bridge_id"] == "zudilin_2002_third_order_zeta5_bridge"
    assert payload["items"][2]["item_id"] == "sequence_level_object"
