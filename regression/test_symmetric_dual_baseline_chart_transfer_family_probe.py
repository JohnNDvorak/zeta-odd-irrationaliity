from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_chart_transfer_family_probe import (
    build_symmetric_dual_baseline_chart_transfer_family_probe,
    render_symmetric_dual_baseline_chart_transfer_family_probe,
    write_symmetric_dual_baseline_chart_transfer_family_probe_json,
    write_symmetric_dual_baseline_chart_transfer_family_probe_report,
)


def test_symmetric_dual_baseline_chart_transfer_family_probe_shows_interpolation_pattern() -> None:
    probe = build_symmetric_dual_baseline_chart_transfer_family_probe()

    assert probe.probe_id == "bz_phase2_symmetric_dual_baseline_chart_transfer_family_probe"
    assert probe.overall_verdict == "bounded_chart_transfer_interpolation_only"
    assert tuple(item.family_id for item in probe.family_results) == (
        "constant_chart_map",
        "difference_chart_map",
        "support1_chart_map",
        "support2_chart_map",
        "support3_chart_map",
        "support4_chart_map",
    )
    assert tuple(item.first_mismatch_index for item in probe.family_results) == (7, 8, 14, 21, 28, 35)


def test_symmetric_dual_baseline_chart_transfer_family_probe_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_symmetric_dual_baseline_chart_transfer_family_probe()

    assert "chart transfer family probe" in report
    assert "support4_chart_map" in report

    report_path = write_symmetric_dual_baseline_chart_transfer_family_probe_report(tmp_path / "probe.md")
    json_path = write_symmetric_dual_baseline_chart_transfer_family_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["family_results"][5]["first_mismatch_index"] == 35
