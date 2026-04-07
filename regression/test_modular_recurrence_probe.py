from __future__ import annotations

from math import factorial

from zeta5_autoresearch.recurrence_mining import modular_rank_certificate


def test_modular_rank_certificate_detects_missing_lower_degree() -> None:
    sequence = tuple(factorial(n) for n in range(13))

    lower = modular_rank_certificate(sequence, degree=0, modulus=1000003)
    exact = modular_rank_certificate(sequence, degree=1, modulus=1000003)

    assert lower.certifies_no_solution is True
    assert exact.certifies_no_solution is False
    assert exact.nullity_upper_bound >= 1
