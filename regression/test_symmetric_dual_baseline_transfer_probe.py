from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_transfer_probe import (
    build_symmetric_dual_baseline_transfer_probe,
    render_symmetric_dual_baseline_transfer_probe,
    write_symmetric_dual_baseline_transfer_probe_json,
    write_symmetric_dual_baseline_transfer_probe_report,
)


def test_symmetric_dual_baseline_transfer_probe_establishes_paired_dual_object() -> None:
    probe = build_symmetric_dual_baseline_transfer_probe()

    assert probe.probe_id == "bz_phase2_symmetric_dual_baseline_transfer_probe"
    assert probe.shared_window_end == 80
    assert probe.verdict == "symmetric_dual_baseline_transfer_object_established"
    assert len(probe.source_packet_hash) == 64
    assert len(probe.target_packet_hash) == 64
    assert len(probe.transfer_object_hash) == 64


def test_symmetric_dual_baseline_transfer_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_dual_baseline_transfer_probe()

    assert "Phase 2 symmetric-dual to baseline-dual transfer probe" in report
    assert "Transfer object hash" in report

    report_path = write_symmetric_dual_baseline_transfer_probe_report(tmp_path / "probe.md")
    json_path = write_symmetric_dual_baseline_transfer_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 80
