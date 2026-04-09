from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_source_packet_compression_probe import (
    build_symmetric_source_packet_compression_probe,
    render_symmetric_source_packet_compression_probe,
    write_symmetric_source_packet_compression_probe_json,
    write_symmetric_source_packet_compression_probe_report,
)


def test_symmetric_source_packet_compression_probe_exhausts_all_pairwise_routes() -> None:
    probe = build_symmetric_source_packet_compression_probe()

    assert probe.probe_id == "bz_phase2_symmetric_source_packet_compression_probe"
    assert probe.overall_verdict == "pairwise_low_complexity_symmetric_source_packet_compression_exhausted"
    assert tuple(item.route_id for item in probe.route_results) == (
        "retain_scaled_q_scaled_p_residual_scaled_phat",
        "retain_scaled_q_scaled_phat_residual_scaled_p",
        "retain_scaled_p_scaled_phat_residual_scaled_q",
    )
    assert tuple(item.first_mismatch_index for item in probe.route_results[0].family_results) == (3, 4, 6)
    assert tuple(item.first_mismatch_index for item in probe.route_results[1].family_results) == (3, 4, 6)
    assert tuple(item.first_mismatch_index for item in probe.route_results[2].family_results) == (3, 4, 6)


def test_symmetric_source_packet_compression_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_source_packet_compression_probe()

    assert "Phase 2 symmetric source packet compression probe" in report
    assert "retain_scaled_q_scaled_p_residual_scaled_phat" in report

    report_path = write_symmetric_source_packet_compression_probe_report(tmp_path / "probe.md")
    json_path = write_symmetric_source_packet_compression_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["route_results"][0]["family_results"][0]["first_mismatch_index"] == 3
