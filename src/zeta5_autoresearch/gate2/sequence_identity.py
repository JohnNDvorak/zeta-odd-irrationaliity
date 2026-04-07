from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Any, Iterable

from ..hashes import compute_sequence_hash
from ..models import fraction_from_scalar, fraction_to_canonical_string


@dataclass(frozen=True)
class ProvisionalSequenceIdentity:
    start_index: int
    order_bound: int
    initial_data: tuple[Fraction, ...]
    signature: tuple[Fraction, ...]

    def to_hash_payload(self) -> dict[str, Any]:
        return {
            "kind": "provisional",
            "start_index": self.start_index,
            "order_bound": self.order_bound,
            "initial_data": [fraction_to_canonical_string(value) for value in self.initial_data],
            "signature": [fraction_to_canonical_string(value) for value in self.signature],
        }

    @classmethod
    def from_scalars(
        cls,
        *,
        start_index: int,
        order_bound: int,
        initial_data: Iterable[Any],
        signature: Iterable[Any],
    ) -> "ProvisionalSequenceIdentity":
        return cls(
            start_index=int(start_index),
            order_bound=int(order_bound),
            initial_data=tuple(fraction_from_scalar(value) for value in initial_data),
            signature=tuple(fraction_from_scalar(value) for value in signature),
        )


@dataclass(frozen=True)
class RecurrenceTerm:
    shift: int
    coefficients: tuple[Fraction, ...]

    @classmethod
    def from_scalars(cls, *, shift: int, coefficients: Iterable[Any]) -> "RecurrenceTerm":
        normalized = tuple(fraction_from_scalar(value) for value in coefficients)
        return cls(shift=int(shift), coefficients=_trim_polynomial(normalized))

    def scaled(self, factor: Fraction) -> "RecurrenceTerm":
        return RecurrenceTerm(shift=self.shift, coefficients=tuple(coefficient * factor for coefficient in self.coefficients))

    def to_hash_payload(self) -> dict[str, Any]:
        return {
            "shift": self.shift,
            "coefficients": [fraction_to_canonical_string(value) for value in self.coefficients],
        }


@dataclass(frozen=True)
class MinimalRecurrenceIdentity:
    start_index: int
    initial_values: tuple[Fraction, ...]
    terms: tuple[RecurrenceTerm, ...]

    def to_hash_payload(self) -> dict[str, Any]:
        return {
            "kind": "minimal_recurrence",
            "start_index": self.start_index,
            "initial_values": [fraction_to_canonical_string(value) for value in self.initial_values],
            "terms": [term.to_hash_payload() for term in self.terms],
        }

    @classmethod
    def from_scalars(
        cls,
        *,
        start_index: int,
        initial_values: Iterable[Any],
        terms: Iterable[RecurrenceTerm],
    ) -> "MinimalRecurrenceIdentity":
        return cls(
            start_index=int(start_index),
            initial_values=tuple(fraction_from_scalar(value) for value in initial_values),
            terms=tuple(terms),
        )


def compute_provisional_sequence_hash(identity: ProvisionalSequenceIdentity) -> str:
    if not identity.signature:
        raise ValueError("provisional sequence identity requires a non-empty exact term signature")
    return compute_sequence_hash(provisional_signature=identity.to_hash_payload())


def compute_verified_sequence_hash(minimal_annihilator: MinimalRecurrenceIdentity) -> str:
    normalized = normalize_minimal_recurrence(minimal_annihilator)
    return compute_sequence_hash(minimal_annihilator=normalized.to_hash_payload())


def normalize_minimal_recurrence(identity: MinimalRecurrenceIdentity) -> MinimalRecurrenceIdentity:
    if not identity.terms:
        raise ValueError("minimal recurrence identity requires at least one term")

    merged_terms: dict[int, list[Fraction]] = {}
    for term in identity.terms:
        trimmed = _trim_polynomial(term.coefficients)
        if _is_zero_polynomial(trimmed):
            continue
        bucket = merged_terms.setdefault(term.shift, [])
        if not bucket:
            bucket.extend(trimmed)
            continue
        if len(bucket) < len(trimmed):
            bucket.extend(Fraction(0) for _ in range(len(trimmed) - len(bucket)))
        for index, value in enumerate(trimmed):
            bucket[index] += value

    normalized_terms = [
        RecurrenceTerm(shift=shift, coefficients=_trim_polynomial(tuple(coefficients)))
        for shift, coefficients in sorted(merged_terms.items())
        if not _is_zero_polynomial(_trim_polynomial(tuple(coefficients)))
    ]
    if not normalized_terms:
        raise ValueError("minimal recurrence identity cannot be identically zero")

    common = _common_rational_content(
        coefficient
        for term in normalized_terms
        for coefficient in term.coefficients
    )
    scaled_terms = [term.scaled(Fraction(1, 1) / common) for term in normalized_terms]

    sign = _leading_sign(scaled_terms)
    if sign < 0:
        scaled_terms = [term.scaled(Fraction(-1, 1)) for term in scaled_terms]

    return MinimalRecurrenceIdentity(
        start_index=identity.start_index,
        initial_values=tuple(identity.initial_values),
        terms=tuple(scaled_terms),
    )


def _trim_polynomial(coefficients: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    trimmed = list(coefficients)
    while trimmed and trimmed[-1] == 0:
        trimmed.pop()
    return tuple(trimmed) if trimmed else (Fraction(0),)


def _is_zero_polynomial(coefficients: tuple[Fraction, ...]) -> bool:
    return all(value == 0 for value in coefficients)


def _common_rational_content(values: Iterable[Fraction]) -> Fraction:
    nonzero = [value for value in values if value != 0]
    if not nonzero:
        return Fraction(1, 1)

    common_denominator = 1
    for value in nonzero:
        common_denominator = _lcm(common_denominator, value.denominator)

    numerators = [abs((value * common_denominator).numerator) for value in nonzero]
    common_numerator = numerators[0]
    for numerator in numerators[1:]:
        common_numerator = gcd(common_numerator, numerator)

    return Fraction(common_numerator, common_denominator)


def _leading_sign(terms: list[RecurrenceTerm]) -> int:
    leading_term = max(terms, key=lambda term: term.shift)
    leading_coefficient = leading_term.coefficients[-1]
    return 1 if leading_coefficient > 0 else -1


def _lcm(left: int, right: int) -> int:
    return abs(left * right) // gcd(left, right)
