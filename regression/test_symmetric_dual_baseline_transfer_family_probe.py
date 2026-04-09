from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_transfer_family_probe import (
    build_symmetric_dual_baseline_transfer_family_probe,
    render_symmetric_dual_baseline_transfer_family_probe,
    write_symmetric_dual_baseline_transfer_family_probe_json,
    write_symmetric_dual_baseline_transfer_family_probe_report,
)


def test_symmetric_dual_baseline_transfer_family_probe_exhausts_low_complexity_ladder() -> None:
    probe = build_symmetric_dual_baseline_transfer_family_probe()

    assert probe.probe_id == "bz_phase2_symmetric_dual_baseline_transfer_family_probe"
    assert probe.overall_verdict == "low_complexity_symmetric_dual_baseline_transfer_exhausted"
    assert tuple(item.family_id for item in probe.family_results) == (
        "constant_packet_map",
        "difference_packet_map",
        "support1_packet_map",
    )
    assert tuple(item.first_mismatch_index for item in probe.family_results) == (4, 5, 8)


def test_symmetric_dual_baseline_transfer_family_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_dual_baseline_transfer_family_probe()

    assert "Phase 2 symmetric-dual to baseline-dual transfer family probe" in report
    assert "constant_packet_map" in report

    report_path = write_symmetric_dual_baseline_transfer_family_probe_report(tmp_path / "probe.md")
    json_path = write_symmetric_dual_baseline_transfer_family_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["family_results"][0]["first_mismatch_index"] == 4
