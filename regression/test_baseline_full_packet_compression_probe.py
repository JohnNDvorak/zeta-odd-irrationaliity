from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_full_packet_compression_probe import (
    build_baseline_full_packet_compression_probe,
    render_baseline_full_packet_compression_probe,
    write_baseline_full_packet_compression_probe_json,
    write_baseline_full_packet_compression_probe_report,
)


def test_baseline_full_packet_compression_probe_exhausts_all_pairwise_routes() -> None:
    probe = build_baseline_full_packet_compression_probe()

    assert probe.probe_id == "bz_phase2_baseline_full_packet_compression_probe"
    assert probe.overall_verdict == "pairwise_low_complexity_packet_compression_exhausted"
    assert tuple(item.route_id for item in probe.route_results) == (
        "retain_constant_zeta5_residual_zeta3",
        "retain_zeta5_zeta3_residual_constant",
        "retain_constant_zeta3_residual_zeta5",
    )
    zeta5_route = probe.route_results[2]
    assert zeta5_route.route_verdict == "hard_wall_low_complexity_zeta5_residual_exhausted"
    assert tuple(item.first_mismatch_index for item in zeta5_route.family_results) == (3, 4, 6)


def test_baseline_full_packet_compression_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_full_packet_compression_probe()

    assert "Phase 2 baseline full-packet compression probe" in report
    assert "retain_constant_zeta3_residual_zeta5" in report

    report_path = write_baseline_full_packet_compression_probe_report(tmp_path / "probe.md")
    json_path = write_baseline_full_packet_compression_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["route_results"][2]["family_results"][0]["first_mismatch_index"] == 3
