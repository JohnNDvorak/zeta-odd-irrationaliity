from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.bz_symmetric_linear_forms_probe import (
    build_bz_totally_symmetric_linear_forms_probe,
    render_bz_totally_symmetric_linear_forms_report,
    write_bz_totally_symmetric_linear_forms_report,
)


def test_totally_symmetric_linear_forms_match_paper_initial_values() -> None:
    probe = build_bz_totally_symmetric_linear_forms_probe(max_n=2, precision=60)

    assert probe.samples[0].q_digits == 1
    assert probe.samples[1].p_numerator_digits == 2
    assert probe.samples[1].p_denominator == 4
    assert probe.samples[1].phat_numerator_digits == 3
    assert probe.samples[1].phat_denominator == 4
    assert probe.samples[2].p_numerator_digits == 7
    assert probe.samples[2].p_denominator == 384
    assert probe.samples[2].phat_numerator_digits == 6
    assert probe.samples[2].phat_denominator == 96


def test_totally_symmetric_linear_forms_recurrence_and_worthiness_probe_hold() -> None:
    probe = build_bz_totally_symmetric_linear_forms_probe(max_n=14, precision=80)

    assert probe.all_p_residuals_zero is True
    assert probe.all_phat_residuals_zero is True
    assert 0.8 < probe.latest_gamma_estimate < 0.9
    assert probe.decay_summary.object_id == "bz_totally_symmetric_remainder_pipeline"
    assert probe.decay_summary.bridge_target_family == "baseline"
    assert probe.decay_summary.exact_status == "mixed"
    assert probe.decay_summary.available_metrics[-1].name == "gamma"


def test_totally_symmetric_linear_forms_report_renders_and_writes(tmp_path: Path) -> None:
    report = render_bz_totally_symmetric_linear_forms_report(max_n=8, precision=70)

    assert "totally symmetric linear-form probe" in report
    assert "worthines" in report

    output = write_bz_totally_symmetric_linear_forms_report(
        max_n=8,
        precision=70,
        output_path=tmp_path / "linear_forms.md",
    )
    contents = output.read_text(encoding="utf-8")

    assert output.exists()
    assert "published initial values" in contents
