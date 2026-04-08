from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_bridge_comparison_probe import (
    build_phase2_external_bridge_comparison_probe,
    render_phase2_external_bridge_comparison_probe,
    write_phase2_external_bridge_comparison_probe_json,
    write_phase2_external_bridge_comparison_probe_report,
)


def test_external_bridge_comparison_probe_classifies_fields() -> None:
    probe = build_phase2_external_bridge_comparison_probe()

    assert probe.probe_id == "bz_phase2_external_bridge_comparison_probe"
    assert probe.bridge_id == "zudilin_2002_third_order_zeta5_bridge"
    assert probe.partial_fields == ("leading_target_channel", "companion_channel")
    assert probe.blocking_fields == ("sequence_level_object",)
    assert any(item.verdict == "blocking_gap" for item in probe.field_verdicts)


def test_external_bridge_comparison_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_bridge_comparison_probe()

    assert "Phase 2 external bridge comparison probe" in report
    assert "structurally_partial" in report
    assert "blocking_gap" in report
    assert "Overall verdict" in report

    report_path = write_phase2_external_bridge_comparison_probe_report(tmp_path / "probe.md")
    json_path = write_phase2_external_bridge_comparison_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["blocking_fields"] == ["sequence_level_object"]
    assert payload["field_verdicts"][0]["field_id"] == "leading_target_channel"
