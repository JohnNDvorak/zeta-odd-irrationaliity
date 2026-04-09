from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_residual_refinement_probe import (
    build_baseline_residual_refinement_probe,
    render_baseline_residual_refinement_probe,
    write_baseline_residual_refinement_probe_json,
    write_baseline_residual_refinement_probe_report,
)


def test_baseline_residual_refinement_probe_exhausts_low_complexity_ladder() -> None:
    probe = build_baseline_residual_refinement_probe()

    assert probe.probe_id == "bz_phase2_baseline_residual_refinement_probe"
    assert probe.overall_verdict == "low_complexity_baseline_refinement_exhausted"
    assert tuple(item.family_id for item in probe.family_results) == (
        "support0_same_index",
        "difference_pair",
        "support1_lagged_pair",
    )
    assert tuple(item.verdict for item in probe.family_results) == (
        "fails_after_fit_window",
        "fails_after_fit_window",
        "fails_after_fit_window",
    )
    assert tuple(item.first_mismatch_index for item in probe.family_results) == (3, 4, 6)
    assert tuple(item.zero_count for item in probe.family_results) == (2, 2, 4)
    assert all(len(item.transformed_residual_hash) == 64 for item in probe.family_results)


def test_baseline_residual_refinement_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_residual_refinement_probe()

    assert "Phase 2 baseline residual refinement probe" in report
    assert "Overall verdict" in report
    assert "Mismatch indices" in report

    report_path = write_baseline_residual_refinement_probe_report(tmp_path / "probe.md")
    json_path = write_baseline_residual_refinement_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["overall_verdict"] == "low_complexity_baseline_refinement_exhausted"
    assert payload["family_results"][0]["mismatch_indices"][0] == 3
    assert payload["family_results"][2]["zero_count"] == 4
