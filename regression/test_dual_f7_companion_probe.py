from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import zeta5_autoresearch.dual_f7_exact_coefficient_cache as cache_module
from zeta5_autoresearch.bz_dual_f7 import (
    compute_f7_constant_signature_from_a,
    compute_f7_constant_term_from_a,
    compute_f7_zeta3_signature_from_a,
    compute_f7_zeta3_term_from_a,
)
from zeta5_autoresearch.bz_dual_f7_companion_probe import (
    build_bz_dual_f7_companion_probe,
    render_bz_dual_f7_companion_probe_report,
)
from zeta5_autoresearch.bz_q_sequence import baseline_a_vector, totally_symmetric_a_vector
from zeta5_autoresearch.dual_f7_exact_coefficient_cache import (
    get_cached_baseline_dual_f7_companion_terms,
    get_cached_baseline_dual_f7_zeta3_terms,
    get_cached_symmetric_dual_f7_constant_terms,
)


def test_companion_exact_component_helpers_match_known_values() -> None:
    assert compute_f7_constant_term_from_a(totally_symmetric_a_vector(), 1) == Fraction(-98, 1)
    assert compute_f7_zeta3_term_from_a(totally_symmetric_a_vector(), 1) == Fraction(66, 1)

    assert compute_f7_constant_signature_from_a(totally_symmetric_a_vector(), term_count=2) == (
        Fraction(-98, 1),
        Fraction(-74463, 16),
    )
    assert compute_f7_zeta3_signature_from_a(totally_symmetric_a_vector(), term_count=2) == (
        Fraction(66, 1),
        Fraction(6125, 2),
    )

    assert compute_f7_zeta3_term_from_a(baseline_a_vector(), 1) == Fraction(-3367966716871959076170056761, 60)


def test_companion_exact_component_caches_roundtrip_small_windows(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline_zeta3.json"
    symmetric_path = tmp_path / "symmetric_constant.json"

    baseline_terms = get_cached_baseline_dual_f7_zeta3_terms(1, cache_path=baseline_path)
    symmetric_terms = get_cached_symmetric_dual_f7_constant_terms(2, cache_path=symmetric_path)

    assert baseline_terms == (Fraction(-3367966716871959076170056761, 60),)
    assert symmetric_terms == (Fraction(-98, 1), Fraction(-74463, 16))

    assert get_cached_baseline_dual_f7_zeta3_terms(1, cache_path=baseline_path) == baseline_terms


def test_companion_pair_cache_extension_reuses_one_linear_form_per_n(tmp_path: Path, monkeypatch) -> None:
    constant_path = tmp_path / "baseline_constant.json"
    zeta3_path = tmp_path / "baseline_zeta3.json"

    tracked_b: list[tuple[int, ...]] = []
    original_extract = cache_module.extract_f7_linear_form

    def tracked_extract(b: tuple[int, ...]):
        tracked_b.append(b)
        return original_extract(b)

    monkeypatch.setattr(cache_module, "extract_f7_linear_form", tracked_extract)

    constant_terms, zeta3_terms = get_cached_baseline_dual_f7_companion_terms(
        2,
        constant_cache_path=constant_path,
        zeta3_cache_path=zeta3_path,
    )

    assert constant_terms == (
        compute_f7_constant_term_from_a(baseline_a_vector(), 1),
        compute_f7_constant_term_from_a(baseline_a_vector(), 2),
    )
    assert zeta3_terms == (
        compute_f7_zeta3_term_from_a(baseline_a_vector(), 1),
        compute_f7_zeta3_term_from_a(baseline_a_vector(), 2),
    )
    assert len(tracked_b) == 2


def test_companion_pair_cache_backfills_lagging_component(tmp_path: Path) -> None:
    constant_path = tmp_path / "baseline_constant.json"
    zeta3_path = tmp_path / "baseline_zeta3.json"

    seeded_zeta3 = get_cached_baseline_dual_f7_zeta3_terms(2, cache_path=zeta3_path)
    constant_terms, zeta3_terms = get_cached_baseline_dual_f7_companion_terms(
        2,
        constant_cache_path=constant_path,
        zeta3_cache_path=zeta3_path,
    )

    assert constant_terms == (
        compute_f7_constant_term_from_a(baseline_a_vector(), 1),
        compute_f7_constant_term_from_a(baseline_a_vector(), 2),
    )
    assert zeta3_terms == seeded_zeta3


def test_dual_f7_companion_probe_renders_small_exact_windows() -> None:
    probe = build_bz_dual_f7_companion_probe(baseline_term_count=1, symmetric_term_count=2)
    baseline_case = next(case for case in probe.cases if case.id == "baseline_bz")
    zeta3_probe = next(component for component in baseline_case.components if component.component == "zeta3")

    assert zeta3_probe.samples[0].denominator_digits == 2
    assert zeta3_probe.samples[0].numerator_digits > 20

    report = render_bz_dual_f7_companion_probe_report(baseline_term_count=1, symmetric_term_count=2)
    assert "dual F_7 companion exact-coefficient probe" in report
    assert "Brown-Zudilin baseline dual companion sequences" in report
