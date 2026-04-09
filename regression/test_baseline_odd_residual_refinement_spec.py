from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_odd_residual_refinement_spec import (
    build_baseline_odd_residual_refinement_spec,
    render_baseline_odd_residual_refinement_spec,
    write_baseline_odd_residual_refinement_spec_json,
    write_baseline_odd_residual_refinement_spec_report,
)


def test_baseline_odd_residual_refinement_spec_freezes_three_fixed_families() -> None:
    spec = build_baseline_odd_residual_refinement_spec()

    assert spec.spec_id == "bz_phase2_baseline_odd_residual_refinement_spec"
    assert spec.shared_window_end == 80
    assert tuple(item.family_id for item in spec.family_specs) == (
        "support0_same_index",
        "difference_pair",
        "support1_lagged_pair",
    )
    assert spec.family_specs[0].family_statement.startswith("r_n = constant_n")


def test_baseline_odd_residual_refinement_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_odd_residual_refinement_spec()

    assert "Phase 2 baseline odd residual refinement spec" in report
    assert "support1_lagged_pair" in report

    report_path = write_baseline_odd_residual_refinement_spec_report(tmp_path / "spec.md")
    json_path = write_baseline_odd_residual_refinement_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["family_specs"][2]["fit_window_end"] == 5
