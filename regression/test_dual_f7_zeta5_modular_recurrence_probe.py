from __future__ import annotations

from zeta5_autoresearch.bz_dual_f7_zeta5_modular_recurrence_probe import (
    build_bz_dual_f7_zeta5_modular_recurrence_probe,
    render_bz_dual_f7_zeta5_modular_recurrence_report,
)


def test_dual_f7_zeta5_modular_recurrence_probe_runs_and_certifies_low_degrees() -> None:
    probe = build_bz_dual_f7_zeta5_modular_recurrence_probe(max_n=20, degrees=(0, 1, 2, 3))

    assert probe.certified_degree_cap is not None
    assert probe.certified_degree_cap >= 1

    report = render_bz_dual_f7_zeta5_modular_recurrence_report(max_n=20, degrees=(0, 1, 2, 3))
    assert "dual F_7 zeta(5)-coefficient modular recurrence certificates" in report
