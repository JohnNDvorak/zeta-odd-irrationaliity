from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_chart_transfer_object_spec import (
    build_symmetric_dual_baseline_chart_transfer_object_spec,
    render_symmetric_dual_baseline_chart_transfer_object_spec,
    write_symmetric_dual_baseline_chart_transfer_object_spec_json,
    write_symmetric_dual_baseline_chart_transfer_object_spec_report,
)


def test_symmetric_dual_baseline_chart_transfer_object_spec_has_expected_window() -> None:
    spec = build_symmetric_dual_baseline_chart_transfer_object_spec()

    assert spec.spec_id == "bz_phase2_symmetric_dual_baseline_chart_transfer_object_spec"
    assert spec.source_profile.shared_window_end == 76
    assert spec.target_profile.shared_window_end == 76


def test_symmetric_dual_baseline_chart_transfer_object_spec_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_symmetric_dual_baseline_chart_transfer_object_spec()

    assert "chart transfer object spec" in report
    assert "window_chart_profile" in report

    report_path = write_symmetric_dual_baseline_chart_transfer_object_spec_report(tmp_path / "spec.md")
    json_path = write_symmetric_dual_baseline_chart_transfer_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_profile"]["shared_window_end"] == 76
