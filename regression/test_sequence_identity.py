from __future__ import annotations

from fractions import Fraction

from zeta5_autoresearch.gate2.sequence_identity import (
    MinimalRecurrenceIdentity,
    ProvisionalSequenceIdentity,
    RecurrenceTerm,
    compute_provisional_sequence_hash,
    compute_verified_sequence_hash,
    normalize_minimal_recurrence,
)
from zeta5_autoresearch.hashes import compute_certificate_hash


def test_verified_sequence_hash_normalizes_scaling_and_term_order() -> None:
    first = MinimalRecurrenceIdentity.from_scalars(
        start_index=0,
        initial_values=[1, 2],
        terms=(
            RecurrenceTerm.from_scalars(shift=1, coefficients=[-2, -4, 0]),
            RecurrenceTerm.from_scalars(shift=0, coefficients=[1, 2, 0]),
        ),
    )
    second = MinimalRecurrenceIdentity.from_scalars(
        start_index=0,
        initial_values=[1, 2],
        terms=(
            RecurrenceTerm.from_scalars(shift=0, coefficients=[-3, -6]),
            RecurrenceTerm.from_scalars(shift=1, coefficients=[6, 12]),
        ),
    )

    normalized = normalize_minimal_recurrence(first)
    assert normalized.terms[0].coefficients == (Fraction(-1, 1), Fraction(-2, 1))
    assert normalized.terms[1].coefficients == (Fraction(2, 1), Fraction(4, 1))
    assert compute_verified_sequence_hash(first) == compute_verified_sequence_hash(second)


def test_provisional_sequence_hash_is_exact_and_format_invariant() -> None:
    first = ProvisionalSequenceIdentity.from_scalars(
        start_index=3,
        order_bound=6,
        initial_data=["1/2", "3/2"],
        signature=["1/2", "3/4", "5/6"],
    )
    second = ProvisionalSequenceIdentity.from_scalars(
        start_index=3,
        order_bound=6,
        initial_data=[Fraction(1, 2), Fraction(3, 2)],
        signature=[Fraction(1, 2), Fraction(3, 4), Fraction(5, 6)],
    )

    assert compute_provisional_sequence_hash(first) == compute_provisional_sequence_hash(second)


def test_certificate_hash_works_once_verified_sequence_hash_exists() -> None:
    recurrence = MinimalRecurrenceIdentity.from_scalars(
        start_index=0,
        initial_values=[1, 2],
        terms=(
            RecurrenceTerm.from_scalars(shift=0, coefficients=[1]),
            RecurrenceTerm.from_scalars(shift=1, coefficients=[-1, -1]),
        ),
    )
    sequence_hash = compute_verified_sequence_hash(recurrence)
    certificate_hash = compute_certificate_hash(
        sequence_hash=sequence_hash,
        representation="cellular_dihedral",
        template="BZ_standard",
        nu_p_method="group_orbit_factorial_ratio",
    )

    assert len(sequence_hash) == 64
    assert len(certificate_hash) == 64
