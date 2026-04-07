from __future__ import annotations

from fractions import Fraction

from zeta5_autoresearch.gate2.recurrence_eval import generate_terms_from_recurrence
from zeta5_autoresearch.gate2.sequence_identity import MinimalRecurrenceIdentity, RecurrenceTerm
from zeta5_autoresearch.recurrence_mining import search_polynomial_recurrences


def test_polynomial_recurrence_search_finds_known_degree() -> None:
    identity = MinimalRecurrenceIdentity.from_scalars(
        start_index=2,
        initial_values=[1, 2, 5],
        terms=(
            RecurrenceTerm.from_scalars(shift=1, coefficients=[2, 1]),
            RecurrenceTerm.from_scalars(shift=0, coefficients=[-5, -3]),
            RecurrenceTerm.from_scalars(shift=-1, coefficients=[1, 2]),
            RecurrenceTerm.from_scalars(shift=-2, coefficients=[0, -1]),
        ),
    )
    sequence = generate_terms_from_recurrence(identity, max_index=12)
    results = search_polynomial_recurrences(sequence, degree_min=0, degree_max=1)

    assert results[0].nullity == 0
    assert results[1].nullity >= 1


def test_first_basis_relation_annihilates_synthetic_sequence() -> None:
    identity = MinimalRecurrenceIdentity.from_scalars(
        start_index=2,
        initial_values=[1, 2, 5],
        terms=(
            RecurrenceTerm.from_scalars(shift=1, coefficients=[2, 1]),
            RecurrenceTerm.from_scalars(shift=0, coefficients=[-5, -3]),
            RecurrenceTerm.from_scalars(shift=-1, coefficients=[1, 2]),
            RecurrenceTerm.from_scalars(shift=-2, coefficients=[0, -1]),
        ),
    )
    sequence = generate_terms_from_recurrence(identity, max_index=12)
    results = search_polynomial_recurrences(sequence, degree_min=1, degree_max=1)
    basis = results[0].basis[0]

    assert basis.coefficient_height > 0
    for n in range(results[0].start_n, results[0].end_n + 1):
        assert basis.evaluate(sequence, n) == Fraction(0)


def test_full_rank_search_can_certify_no_solution_without_basis() -> None:
    sequence = tuple(Fraction(n**3 + 2 * n + 1) for n in range(12))

    result = search_polynomial_recurrences(sequence, degree_min=0, degree_max=0)[0]

    assert result.rank == result.variable_count == 4
    assert result.nullity == 0
    assert result.basis == ()
