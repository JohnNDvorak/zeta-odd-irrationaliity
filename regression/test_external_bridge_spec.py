from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.external_bridge_spec import (
    build_phase2_external_bridge_spec,
    render_phase2_external_bridge_spec,
    write_phase2_external_bridge_spec_json,
    write_phase2_external_bridge_spec_report,
)


def test_external_bridge_spec_uses_zudilin_2002_bridge() -> None:
    spec = build_phase2_external_bridge_spec()

    assert spec.spec_id == "bz_phase2_external_bridge_spec"
    assert spec.bridge_id == "zudilin_2002_third_order_zeta5_bridge"
    assert "third-order Apéry-like recursion" in spec.source
    assert len(spec.comparison_fields) == 3
    assert spec.comparison_fields[0].field_id == "leading_target_channel"
    assert "published recurrence-based linear forms" in spec.bridge_object.lower()


def test_external_bridge_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_external_bridge_spec()

    assert "Phase 2 external bridge spec" in report
    assert "zudilin_2002_third_order_zeta5_bridge" in report
    assert "Comparison fields" in report
    assert "leading_target_channel" in report

    report_path = write_phase2_external_bridge_spec_report(tmp_path / "bridge.md")
    json_path = write_phase2_external_bridge_spec_json(tmp_path / "bridge.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["bridge_id"] == "zudilin_2002_third_order_zeta5_bridge"
    assert payload["comparison_fields"][1]["field_id"] == "companion_channel"
