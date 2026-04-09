from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_full_packet_object_spec import (
    build_baseline_full_packet_object_spec,
    render_baseline_full_packet_object_spec,
    write_baseline_full_packet_object_spec_json,
    write_baseline_full_packet_object_spec_report,
)


def test_baseline_full_packet_object_spec_keeps_all_three_channels_active() -> None:
    spec = build_baseline_full_packet_object_spec()

    assert spec.spec_id == "bz_phase2_baseline_full_packet_object_spec"
    assert tuple(item.component_id for item in spec.components) == ("constant", "zeta3", "zeta5")
    assert "full coefficient packet" in spec.rationale
    assert spec.components[2].max_verified_index == 80


def test_baseline_full_packet_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_full_packet_object_spec()

    assert "Phase 2 baseline full-packet object spec" in report
    assert "zeta5" in report
    assert "pairwise compression" in report

    report_path = write_baseline_full_packet_object_spec_report(tmp_path / "spec.md")
    json_path = write_baseline_full_packet_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["components"][1]["component_id"] == "zeta3"
