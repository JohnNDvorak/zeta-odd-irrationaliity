from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_odd_pair_object_spec import (
    build_baseline_odd_pair_object_spec,
    render_baseline_odd_pair_object_spec,
    write_baseline_odd_pair_object_spec_json,
    write_baseline_odd_pair_object_spec_report,
)


def test_baseline_odd_pair_object_spec_chooses_odd_weight_pair() -> None:
    spec = build_baseline_odd_pair_object_spec()

    assert spec.spec_id == "bz_phase2_baseline_odd_pair_object_spec"
    assert tuple(item.component_id for item in spec.components) == (
        "retained_zeta5",
        "retained_zeta3",
        "residual_constant",
    )
    assert "odd-zeta channels together" in spec.rationale
    assert spec.components[0].max_verified_index == 80


def test_baseline_odd_pair_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_baseline_odd_pair_object_spec()

    assert "Phase 2 baseline odd-pair object spec" in report
    assert "retained_zeta5" in report
    assert "residual_constant" in report

    report_path = write_baseline_odd_pair_object_spec_report(tmp_path / "spec.md")
    json_path = write_baseline_odd_pair_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["components"][1]["component_id"] == "retained_zeta3"
