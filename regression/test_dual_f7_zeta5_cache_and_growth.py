from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.bz_dual_f7_zeta5_growth_probe import build_bz_dual_f7_zeta5_growth_probe, render_bz_dual_f7_zeta5_growth_report
from zeta5_autoresearch.dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms, get_cached_symmetric_dual_f7_zeta5_terms


def test_dual_f7_zeta5_cache_roundtrips_known_prefix(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    symmetric_path = tmp_path / "symmetric.json"

    baseline_terms = get_cached_baseline_dual_f7_zeta5_terms(4, cache_path=baseline_path)
    symmetric_terms = get_cached_symmetric_dual_f7_zeta5_terms(4, cache_path=symmetric_path)

    assert baseline_terms[:2] == (
        -17062318711073217087874368,
        152044985550430960231949449314536670627277608934680000,
    )
    assert symmetric_terms == (18, 938, 77202, 8017002)

    assert get_cached_baseline_dual_f7_zeta5_terms(3, cache_path=baseline_path) == baseline_terms[:3]


def test_dual_f7_zeta5_growth_probe_renders() -> None:
    probe = build_bz_dual_f7_zeta5_growth_probe(max_n=8)

    assert probe.latest_root_estimate > 60
    assert probe.latest_ratio_estimate > 1

    report = render_bz_dual_f7_zeta5_growth_report(max_n=8)
    assert "dual F_7 zeta(5)-coefficient growth probe" in report
