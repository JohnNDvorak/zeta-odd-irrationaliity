from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_full_packet_probe import (
    build_baseline_full_packet_probe,
    render_baseline_full_packet_probe,
    write_baseline_full_packet_probe_json,
    write_baseline_full_packet_probe_report,
)


def test_baseline_full_packet_probe_establishes_full_packet() -> None:
    probe = build_baseline_full_packet_probe()

    assert probe.probe_id == "bz_phase2_baseline_full_packet_probe"
    assert probe.shared_window_end == 80
    assert probe.verdict == "baseline_full_packet_established"
    assert len(probe.packet_hash) == 64


def test_baseline_full_packet_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_full_packet_probe()

    assert "Phase 2 baseline full-packet probe" in report
    assert "Packet hash" in report

    report_path = write_baseline_full_packet_probe_report(tmp_path / "probe.md")
    json_path = write_baseline_full_packet_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 80
