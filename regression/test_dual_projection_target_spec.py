from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.dual_projection_target_spec import (
    build_phase2_dual_projection_target_spec,
    render_phase2_dual_projection_target_spec,
    write_phase2_dual_projection_target_spec_json,
    write_phase2_dual_projection_target_spec_report,
)


def test_dual_projection_target_spec_uses_exact_coefficient_packet() -> None:
    spec = build_phase2_dual_projection_target_spec()

    assert spec.target_id == "baseline_dual_f7_exact_coefficient_packet"
    assert spec.target_kind == "pre_projection_exact_coefficient_packet"
    assert spec.baseline_seed == "a=(8,16,10,15,12,16,18,13)"
    assert [component.component_id for component in spec.components] == ["constant", "zeta3", "zeta5"]
    assert spec.components[0].max_verified_index >= spec.components[2].max_verified_index
    assert any("not a published baseline P_n sequence" in item for item in spec.non_claims)


def test_dual_projection_target_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_dual_projection_target_spec()

    assert "Phase 2 dual projection target spec" in report
    assert "Baseline dual F_7 exact coefficient packet" in report
    assert "pre_projection_exact_coefficient_packet" in report
    assert "constant" in report and "zeta3" in report and "zeta5" in report

    report_path = write_phase2_dual_projection_target_spec_report(tmp_path / "target.md")
    json_path = write_phase2_dual_projection_target_spec_json(tmp_path / "target.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["target_id"] == "baseline_dual_f7_exact_coefficient_packet"
    assert payload["components"][2]["component_id"] == "zeta5"
