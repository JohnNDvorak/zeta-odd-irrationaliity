from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_transfer_object_spec import (
    build_symmetric_dual_baseline_transfer_object_spec,
    render_symmetric_dual_baseline_transfer_object_spec,
    write_symmetric_dual_baseline_transfer_object_spec_json,
    write_symmetric_dual_baseline_transfer_object_spec_report,
)


def test_symmetric_dual_baseline_transfer_object_spec_pairs_dual_packets() -> None:
    spec = build_symmetric_dual_baseline_transfer_object_spec()

    assert spec.spec_id == "bz_phase2_symmetric_dual_baseline_transfer_object_spec"
    assert spec.source_packet.packet_id == "bz_phase2_symmetric_dual_full_packet"
    assert spec.target_packet.packet_id == "bz_phase2_baseline_full_packet"
    assert spec.source_packet.shared_window_end == 80
    assert spec.target_packet.shared_window_end == 80


def test_symmetric_dual_baseline_transfer_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_dual_baseline_transfer_object_spec()

    assert "Phase 2 symmetric-dual to baseline-dual transfer object spec" in report
    assert "Symmetric-dual to baseline-dual transfer object" in report

    report_path = write_symmetric_dual_baseline_transfer_object_spec_report(tmp_path / "spec.md")
    json_path = write_symmetric_dual_baseline_transfer_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_packet"]["packet_id"] == "bz_phase2_symmetric_dual_full_packet"
