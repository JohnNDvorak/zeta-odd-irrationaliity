from __future__ import annotations

from zeta5_autoresearch.bz_dual_f7_companion_normalization_probe import (
    build_bz_dual_f7_companion_normalization_probe,
    render_bz_dual_f7_companion_normalization_report,
)


def test_dual_f7_companion_normalization_probe_builds_cleared_caps() -> None:
    probe = build_bz_dual_f7_companion_normalization_probe(max_n=20, degree_min=0, degree_max=4)

    assert len(probe.components) == 2
    for component in probe.components:
        assert component.window_scale_digits > 0
        assert component.exact_no_solution_degree_cap == 3
        assert component.first_compatible_degree == 4


def test_dual_f7_companion_normalization_report_renders() -> None:
    report = render_bz_dual_f7_companion_normalization_report(max_n=20, degree_min=0, degree_max=4)

    assert "dual F_7 companion normalization probe" in report
    assert "Window common denominator digits" in report
    assert "Cleared-window no-solution cap" in report


def test_dual_f7_companion_normalization_report_handles_large_digit_counts() -> None:
    report = render_bz_dual_f7_companion_normalization_report(max_n=71, degree_min=0, degree_max=16)

    assert "loaded through `n=71`" in report
    assert "Cleared-term digit count at `n=71`" in report


def test_dual_f7_companion_normalization_report_handles_large_denominator_digits() -> None:
    report = render_bz_dual_f7_companion_normalization_report(max_n=191, degree_min=0, degree_max=0)

    assert "loaded through `n=191`" in report
    assert "First six denominator-digit counts" in report
