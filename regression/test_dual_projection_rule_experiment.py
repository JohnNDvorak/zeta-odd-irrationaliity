from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.dual_projection_rule_experiment import (
    build_phase2_dual_projection_rule_experiment,
    render_phase2_dual_projection_rule_experiment,
    write_phase2_dual_projection_rule_experiment_report,
)


def test_dual_projection_rule_experiment_splits_retained_pair_and_residual() -> None:
    experiment = build_phase2_dual_projection_rule_experiment()

    assert experiment.rule_id == "keep_constant_and_zeta5_carry_zeta3_residual_v1"
    assert experiment.shared_window_end == 80
    assert len(experiment.retained_pair_hash) == 64
    assert len(experiment.residual_channel_hash) == 64
    assert experiment.packet_source_hash != experiment.retained_pair_hash
    assert any("bookkeeping-only" in item for item in experiment.departures_from_calibration)
    assert experiment.samples[0].n == 1


def test_dual_projection_rule_experiment_report_renders_and_writes(tmp_path: Path) -> None:
    report = render_phase2_dual_projection_rule_experiment()

    assert "Phase 2 dual projection rule experiment" in report
    assert "retained pair hash" in report.lower()
    assert "residual channel hash" in report.lower()
    assert "Sample retained / residual data" in report
    assert "bookkeeping projection rule" in report

    output = write_phase2_dual_projection_rule_experiment_report(tmp_path / "rule.md")
    assert output.exists()
    assert "keep_constant_and_zeta5_carry_zeta3_residual_v1" in output.read_text(encoding="utf-8")
