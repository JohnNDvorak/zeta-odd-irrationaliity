from __future__ import annotations

from zeta5_autoresearch.bz_q_sequence import (
    baseline_a_vector,
    build_modular_binomial_table_for_a,
    compute_q_signature_from_a,
    compute_q_signature_from_a_mod,
    totally_symmetric_a_vector,
)


def test_modular_q_signature_matches_exact_baseline_signature() -> None:
    modulus = 1000003
    table = build_modular_binomial_table_for_a(baseline_a_vector(), 7, modulus=modulus)

    exact = compute_q_signature_from_a(baseline_a_vector(), term_count=8)
    modular = compute_q_signature_from_a_mod(
        baseline_a_vector(),
        modulus=modulus,
        term_count=8,
        table=table,
    )

    assert modular == tuple(value % modulus for value in exact)


def test_modular_q_signature_matches_exact_symmetric_signature() -> None:
    modulus = 1000033
    table = build_modular_binomial_table_for_a(totally_symmetric_a_vector(), 5, modulus=modulus)

    exact = compute_q_signature_from_a(totally_symmetric_a_vector(), term_count=6)
    modular = compute_q_signature_from_a_mod(
        totally_symmetric_a_vector(),
        modulus=modulus,
        term_count=6,
        table=table,
    )

    assert modular == tuple(value % modulus for value in exact)
