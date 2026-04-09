from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_affine_normalization_map_probe import (
    build_zudilin_2002_affine_normalization_map_probe,
    render_zudilin_2002_affine_normalization_map_probe,
    write_zudilin_2002_affine_normalization_map_probe_json,
    write_zudilin_2002_affine_normalization_map_probe_report,
)


def test_zudilin_2002_affine_normalization_map_probe_rejects_affine_map() -> None:
    probe = build_zudilin_2002_affine_normalization_map_probe(max_n=7)

    assert probe.probe_id == "bz_phase2_zudilin_2002_affine_normalization_map_probe"
    assert probe.shared_window_end == 7
    assert probe.verdict == "affine_scalar_map_fails"
    assert probe.mismatch_indices
    assert probe.samples[0].matches_affine_candidate is True
    assert probe.samples[1].matches_affine_candidate is True


def test_zudilin_2002_affine_normalization_map_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_affine_normalization_map_probe(max_n=7)

    assert "Phase 2 Zudilin 2002 affine normalization map probe" in report
    assert "affine_scalar_map_fails" in report
    assert "predicted affine ratio" in report

    report_path = write_zudilin_2002_affine_normalization_map_probe_report(
        max_n=7, output_path=tmp_path / "affine.md"
    )
    json_path = write_zudilin_2002_affine_normalization_map_probe_json(max_n=7, output_path=tmp_path / "affine.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["verdict"] == "affine_scalar_map_fails"
    assert payload["shared_window_end"] == 7
