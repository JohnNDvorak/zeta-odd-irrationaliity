from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .sequence_identity import MinimalRecurrenceIdentity, RecurrenceTerm


@dataclass(frozen=True)
class RecurrenceResidual:
    n: int
    residual: Fraction

    @property
    def vanishes(self) -> bool:
        return self.residual == 0


def evaluate_polynomial(coefficients: tuple[Fraction, ...], n: int) -> Fraction:
    value = Fraction(0)
    power = Fraction(1)
    for coefficient in coefficients:
        value += coefficient * power
        power *= n
    return value


def initial_index_range(identity: MinimalRecurrenceIdentity) -> tuple[int, int]:
    min_shift = min(term.shift for term in identity.terms)
    max_shift = max(term.shift for term in identity.terms)
    lower = identity.start_index + min_shift
    upper = identity.start_index + max_shift - 1
    return lower, upper


def generate_terms_from_recurrence(identity: MinimalRecurrenceIdentity, *, max_index: int) -> tuple[Fraction, ...]:
    lower, upper = initial_index_range(identity)
    expected_initial_count = upper - lower + 1
    if expected_initial_count <= 0:
        raise ValueError("minimal recurrence must have positive initial span")
    if len(identity.initial_values) != expected_initial_count:
        raise ValueError(
            "initial_values length does not match recurrence span: "
            f"expected {expected_initial_count}, got {len(identity.initial_values)}"
        )
    if max_index < upper:
        raise ValueError(f"max_index must be at least {upper}")

    values = {lower + offset: value for offset, value in enumerate(identity.initial_values)}
    leading = max(identity.terms, key=lambda term: term.shift)
    others = tuple(term for term in identity.terms if term is not leading)

    for n in range(identity.start_index, max_index - leading.shift + 1):
        target_index = n + leading.shift
        if target_index in values:
            continue
        leading_value = evaluate_polynomial(leading.coefficients, n)
        if leading_value == 0:
            raise ZeroDivisionError(f"leading recurrence coefficient vanishes at n={n}")
        residual = Fraction(0)
        for term in others:
            source_index = n + term.shift
            if source_index not in values:
                raise ValueError(f"recurrence requires missing value at index {source_index}")
            residual += evaluate_polynomial(term.coefficients, n) * values[source_index]
        values[target_index] = -residual / leading_value

    return tuple(values[index] for index in range(lower, max_index + 1))


def recurrence_residuals(
    identity: MinimalRecurrenceIdentity,
    *,
    values_by_index: dict[int, Fraction],
    start_n: int | None = None,
    end_n: int,
) -> tuple[RecurrenceResidual, ...]:
    lower_n = identity.start_index if start_n is None else start_n
    residuals = []
    for n in range(lower_n, end_n + 1):
        total = Fraction(0)
        for term in identity.terms:
            index = n + term.shift
            if index not in values_by_index:
                raise ValueError(f"missing sequence value at index {index}")
            total += evaluate_polynomial(term.coefficients, n) * values_by_index[index]
        residuals.append(RecurrenceResidual(n=n, residual=total))
    return tuple(residuals)
