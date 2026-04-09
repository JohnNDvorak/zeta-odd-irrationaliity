from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_pair_object_spec import (
    build_baseline_pair_object_spec,
    render_baseline_pair_object_spec,
    write_baseline_pair_object_spec_json,
    write_baseline_pair_object_spec_report,
)


def test_baseline_pair_object_spec_is_repo_native_and_bridge_bounded() -> None:
    spec = build_baseline_pair_object_spec()

    assert spec.spec_id == "bz_phase2_baseline_pair_object_spec"
    assert spec.source_packet_id == "baseline_dual_f7_exact_coefficient_packet"
    assert spec.object_kind == "baseline_side_exact_pair_with_explicit_residual"
    assert len(spec.components) == 3
    assert "calibration" in spec.bridge_boundary
    assert "baseline P_n extraction" in spec.non_claims[2]


def test_baseline_pair_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_pair_object_spec()

    assert "Phase 2 baseline pair object spec" in report
    assert "Object semantics" in report
    assert "Extraction output type" in report

    report_path = write_baseline_pair_object_spec_report(tmp_path / "spec.md")
    json_path = write_baseline_pair_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_packet_id"] == "baseline_dual_f7_exact_coefficient_packet"
    assert payload["components"][0]["component_id"] == "retained_constant"
