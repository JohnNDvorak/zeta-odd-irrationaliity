from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.bz_growth_probe import (
    build_bz_baseline_growth_probe,
    render_bz_baseline_growth_report,
    write_bz_baseline_growth_report,
)


def test_bz_growth_probe_validates_seeded_evidence() -> None:
    probe = build_bz_baseline_growth_probe(max_n=8)

    assert probe.evidence_signature_match is True
    assert probe.evidence_initial_data_match is True
    assert len(probe.samples) == 9
    assert probe.samples[-1].log_abs_ratio_est is not None


def test_bz_growth_probe_accelerated_c1_tracks_fixture() -> None:
    probe = build_bz_baseline_growth_probe(max_n=20)

    assert abs(probe.latest_accelerated_c1_delta) < 0.005
    assert probe.latest_accelerated_c1_estimate > probe.latest_ratio_estimate > probe.latest_root_estimate


def test_bz_growth_report_renders_and_writes(tmp_path: Path) -> None:
    report = render_bz_baseline_growth_report(max_n=8)

    assert "# Brown-Zudilin baseline Q_n growth probe" in report
    assert "uncertified numeric calibration" in report
    assert "Latest accelerated `C1` estimate" in report

    output = write_bz_baseline_growth_report(max_n=8, output_path=tmp_path / "growth.md")
    contents = output.read_text(encoding="utf-8")

    assert output.exists()
    assert "Seeded signature check: `pass`" in contents
