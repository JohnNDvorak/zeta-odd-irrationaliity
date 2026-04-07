from __future__ import annotations

from zeta5_autoresearch.bz_dual_f7_companion_recurrence_probe import (
    build_bz_dual_f7_companion_recurrence_probe,
    render_bz_dual_f7_companion_recurrence_report,
)


def test_dual_f7_companion_recurrence_probe_builds_exact_no_solution_caps() -> None:
    probe = build_bz_dual_f7_companion_recurrence_probe(max_n=12, degree_min=0, degree_max=2)

    assert len(probe.components) == 2
    for component in probe.components:
        assert component.exact_no_solution_degree_cap == 1
        assert component.first_compatible_degree == 2


def test_dual_f7_companion_recurrence_report_renders() -> None:
    report = render_bz_dual_f7_companion_recurrence_report(max_n=12, degree_min=0, degree_max=2)

    assert "dual F_7 companion exact-sequence recurrence probe" in report
    assert "Constant Sequence" in report
    assert "zeta(3) Coefficient Sequence" in report
