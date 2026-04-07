from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_q_cache import (
    get_cached_baseline_q_terms,
    get_cached_baseline_q_terms_as_fractions,
    get_cached_baseline_q_terms_mod_prime,
)
from zeta5_autoresearch.bz_q_sequence import baseline_a_vector, compute_q_signature_from_a


def test_baseline_q_cache_writes_and_reuses_terms(tmp_path: Path) -> None:
    cache_path = tmp_path / "baseline_terms.json"

    first = get_cached_baseline_q_terms(6, cache_path=cache_path)
    second = get_cached_baseline_q_terms(4, cache_path=cache_path)
    extended = get_cached_baseline_q_terms(8, cache_path=cache_path)
    payload = json.loads(cache_path.read_text(encoding="utf-8"))

    assert first[:5] == second
    assert extended[:7] == first
    assert payload["max_n"] == 8
    assert len(payload["terms"]) == 9


def test_baseline_q_cache_fraction_view_is_exact(tmp_path: Path) -> None:
    cache_path = tmp_path / "baseline_terms.json"
    values = get_cached_baseline_q_terms_as_fractions(3, cache_path=cache_path)

    assert tuple(value.denominator for value in values) == (1, 1, 1, 1)


def test_baseline_q_mod_cache_matches_exact_terms_mod_prime(tmp_path: Path) -> None:
    cache_path = tmp_path / "baseline_terms_mod_1000003.json"
    modulus = 1000003

    first = get_cached_baseline_q_terms_mod_prime(6, modulus=modulus, cache_path=cache_path)
    second = get_cached_baseline_q_terms_mod_prime(4, modulus=modulus, cache_path=cache_path)
    extended = get_cached_baseline_q_terms_mod_prime(8, modulus=modulus, cache_path=cache_path)
    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    exact = compute_q_signature_from_a(baseline_a_vector(), term_count=9)

    assert first[:5] == second
    assert extended[:7] == first
    assert tuple(value % modulus for value in exact) == extended
    assert payload["modulus"] == modulus
    assert payload["max_n"] == 8
