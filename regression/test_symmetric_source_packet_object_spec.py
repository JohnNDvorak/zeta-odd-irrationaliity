from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_source_packet_object_spec import (
    build_symmetric_source_packet_object_spec,
    render_symmetric_source_packet_object_spec,
    write_symmetric_source_packet_object_spec_json,
    write_symmetric_source_packet_object_spec_report,
)


def test_symmetric_source_packet_object_spec_uses_scaled_source_family() -> None:
    spec = build_symmetric_source_packet_object_spec()

    assert spec.spec_id == "bz_phase2_symmetric_source_packet_object_spec"
    assert spec.source_family == "totally_symmetric_linear_form_pipeline"
    assert tuple(component.component_id for component in spec.components) == (
        "scaled_q",
        "scaled_p",
        "scaled_phat",
    )
    assert all(component.max_verified_index == 80 for component in spec.components)


def test_symmetric_source_packet_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_symmetric_source_packet_object_spec()

    assert "Phase 2 symmetric source packet object spec" in report
    assert "Totally symmetric scaled coefficient packet" in report

    report_path = write_symmetric_source_packet_object_spec_report(tmp_path / "spec.md")
    json_path = write_symmetric_source_packet_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["components"][0]["component_id"] == "scaled_q"
