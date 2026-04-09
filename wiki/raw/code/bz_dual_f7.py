from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache, reduce
from math import comb, gcd

import mpmath

try:
    import gmpy2
except ImportError:  # pragma: no cover - optional acceleration backend
    gmpy2 = None

from .models import fraction_to_canonical_string


@dataclass(frozen=True)
class DualF7Relation:
    coefficients: tuple[int, int, int, int]
    constant_term: Fraction
    zeta3_coeff: Fraction
    zeta5_coeff: Fraction
    residual_log10_abs: float | None


@dataclass(frozen=True)
class ExactDualF7LinearForm:
    b: tuple[int, ...]
    constant_term: Fraction
    zeta_coefficients: tuple[tuple[int, Fraction], ...]

    def zeta_coefficient(self, weight: int) -> Fraction:
        for candidate_weight, coefficient in self.zeta_coefficients:
            if candidate_weight == weight:
                return coefficient
        return Fraction(0)


@dataclass
class _HarmonicPowerTable:
    numerators: list[int]
    denominators: list[int]
    reduced_values: list[Fraction | None]


@dataclass(frozen=True)
class _FactorizedRational:
    sign: int
    prime_exponents: tuple[tuple[int, int], ...]


DUAL_F7_COMPONENTS = frozenset({"constant", "zeta3", "zeta5"})
_HARMONIC_NUMBER_TABLES: dict[int, _HarmonicPowerTable] = {}
_FACTORIAL_TABLE: list[int] = [1]
_SMALLEST_PRIME_FACTOR_TABLE: list[int] = [0, 1]
_PRIME_FACTORIZATION_TABLE: list[tuple[tuple[int, int], ...]] = [(), ()]
_FACTORIAL_PRIME_EXPONENT_TABLE: list[tuple[tuple[int, int], ...]] = [(), ()]
_FRACTION_PAIR_SELECTION_WINDOW = 6
_NUMERATOR_GCD_BIT_LENGTH_CUTOFF = 4096
_NUMERATOR_GCD_BIT_LENGTH_CUTOFF_WITH_GMPY2 = 1_000_000
_REDUCTION_GCD_BIT_LENGTH_CUTOFF = 4096
_MULTIPLICATION_GCD_BIT_LENGTH_CUTOFF = 4096
_BACKEND_MULTIPLICATION_BIT_LENGTH_CUTOFF = 1_000_000
_FACTOR_PAIR_PRODUCT_CACHE_BIT_LENGTH_CUTOFF = 32768
_ADDITION_QUOTIENT_BIT_LENGTH_CUTOFF = 4096
_PAIR_GCD_DIVISIBILITY_BIT_LENGTH_CUTOFF = 4096
_FINAL_SUM_NORMALIZATION_GCD_BIT_LENGTH_CUTOFF = 4096
_BACKEND_ADD_REDUCTION_GCD_BIT_LENGTH_CUTOFF = 1_000_000
_PAIR_GCD_FALLBACK_SKIP_BIT_LENGTH_CUTOFF = 8192
_PRIME_STRIP_SMALL_QUOTIENT_BIT_LENGTH_CUTOFF = 4096
_PRIME_STRIP_REMOVE_BIT_LENGTH_CUTOFF = 4096
_RATIONAL_BACKEND_ADDITION_BIT_LENGTH_CUTOFF = 32768
_MPQ_CONVERSION_CACHE_BIT_LENGTH_CUTOFF = 32768
_MPQ_SUM_DENOMINATOR_BIT_LENGTH_CUTOFF = 32768
_MPQ_COMPONENT_SUM_DENOMINATOR_BIT_LENGTH_CUTOFF = 32768
_MPQ_EXP_SERIES_BIT_LENGTH_CUTOFF = 4096


def _exact_gcd(left: int, right: int) -> int:
    if gmpy2 is None:
        return gcd(left, right)
    return int(gmpy2.gcd(left, right))


def _exact_product(left: int, right: int) -> int:
    if gmpy2 is None:
        return left * right
    return int(gmpy2.mpz(left) * right)


def _exact_quotient(value: int, divisor: int) -> int:
    if gmpy2 is None:
        return value // divisor
    return int(gmpy2.mpz(value) // divisor)


def dual_b_vector_from_a(a: tuple[int, ...]) -> tuple[int, ...]:
    if len(a) != 8:
        raise ValueError("a must have length 8")
    a1, a2, a3, a4, a5, a6, a7, a8 = a
    b = (
        a2 + a3 + a4,
        -a1 + a3 + a4,
        a2,
        a4,
        a2 + a3 - a5,
        a2 + a3 - a8,
        a4 - a6 + a8,
        a2 + a3 + a6 - a7 - a8,
    )
    _validate_b_vector(b)
    return b


def scale_b_vector(b: tuple[int, ...], n: int) -> tuple[int, ...]:
    if len(b) != 8:
        raise ValueError("b must have length 8")
    if n < 0:
        raise ValueError("n must be nonnegative")
    scaled = tuple(value * n for value in b)
    _validate_b_vector(scaled)
    return scaled


def scaled_dual_b_vector_from_a(a: tuple[int, ...], n: int) -> tuple[int, ...]:
    return scale_b_vector(dual_b_vector_from_a(a), n)


def compute_f7_zeta5_term_from_a(a: tuple[int, ...], n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    return extract_f7_zeta5_coefficient(scale_b_vector(dual_b_vector_from_a(a), n))


def compute_f7_exact_component_term_from_a(a: tuple[int, ...], n: int, *, component: str) -> Fraction:
    if n <= 0:
        raise ValueError("n must be positive")
    normalized_component = _normalize_component_label(component)
    if normalized_component == "zeta5":
        return Fraction(compute_f7_zeta5_term_from_a(a, n))

    linear_form = extract_f7_linear_form(scale_b_vector(dual_b_vector_from_a(a), n))
    if normalized_component == "constant":
        return linear_form.constant_term
    return linear_form.zeta_coefficient(3)


def compute_f7_constant_term_from_a(a: tuple[int, ...], n: int) -> Fraction:
    return compute_f7_exact_component_term_from_a(a, n, component="constant")


def compute_f7_zeta3_term_from_a(a: tuple[int, ...], n: int) -> Fraction:
    return compute_f7_exact_component_term_from_a(a, n, component="zeta3")


def compute_f7_zeta5_signature_from_a(
    a: tuple[int, ...],
    *,
    start_index: int = 1,
    term_count: int = 6,
) -> tuple[int, ...]:
    if start_index <= 0:
        raise ValueError("start_index must be positive")
    if term_count <= 0:
        raise ValueError("term_count must be positive")
    return tuple(compute_f7_zeta5_term_from_a(a, start_index + offset) for offset in range(term_count))


def compute_f7_exact_component_signature_from_a(
    a: tuple[int, ...],
    *,
    component: str,
    start_index: int = 1,
    term_count: int = 6,
) -> tuple[Fraction, ...]:
    if start_index <= 0:
        raise ValueError("start_index must be positive")
    if term_count <= 0:
        raise ValueError("term_count must be positive")
    return tuple(
        compute_f7_exact_component_term_from_a(a, start_index + offset, component=component)
        for offset in range(term_count)
    )


def compute_f7_constant_signature_from_a(
    a: tuple[int, ...],
    *,
    start_index: int = 1,
    term_count: int = 6,
) -> tuple[Fraction, ...]:
    return compute_f7_exact_component_signature_from_a(
        a,
        component="constant",
        start_index=start_index,
        term_count=term_count,
    )


def compute_f7_zeta3_signature_from_a(
    a: tuple[int, ...],
    *,
    start_index: int = 1,
    term_count: int = 6,
) -> tuple[Fraction, ...]:
    return compute_f7_exact_component_signature_from_a(
        a,
        component="zeta3",
        start_index=start_index,
        term_count=term_count,
    )


def tilde_f7_prefactor(b: tuple[int, ...]) -> Fraction:
    _validate_b_vector(b)
    b0, *tail = b
    numerator = _exact_factorial(b0 + 1)
    denominator = 1
    for value in tail:
        numerator *= _exact_factorial(value)
        denominator *= _exact_factorial(b0 - value + 1)
    return Fraction(numerator, denominator)


def f7_arithmetic_renormalization(b: tuple[int, ...]) -> Fraction:
    _validate_b_vector(b)
    numerator_factorials, denominator_factorials = _f7_arithmetic_renormalization_factorials(b)
    return _factorial_argument_ratio_fraction(
        numerator_factorials=numerator_factorials,
        denominator_factorials=denominator_factorials,
    )


def evaluate_tilde_f7_hyper_line(b: tuple[int, ...], *, precision: int = 120) -> mpmath.mpf:
    _validate_b_vector(b)
    if precision < 40:
        raise ValueError("precision must be at least 40 decimal digits")
    b0, *tail = b
    with mpmath.workdps(precision):
        prefactor = _mp_fraction(tilde_f7_prefactor(b))
        upper = [b0 + 2, mpmath.mpf(b0) / 2 + 2] + [value + 1 for value in tail]
        lower = [mpmath.mpf(b0) / 2 + 1] + [b0 - value + 2 for value in tail]
        return prefactor * mpmath.hyper(upper, lower, 1)


def evaluate_tilde_f7(b: tuple[int, ...], *, precision: int = 120) -> mpmath.mpf:
    return mpmath.mpf(b[0] + 2) * evaluate_tilde_f7_hyper_line(b, precision=precision)


def evaluate_f7_hyper_line(b: tuple[int, ...], *, precision: int = 120) -> mpmath.mpf:
    with mpmath.workdps(precision):
        return _mp_fraction(f7_arithmetic_renormalization(b)) * evaluate_tilde_f7_hyper_line(b, precision=precision)


def evaluate_f7(b: tuple[int, ...], *, precision: int = 120) -> mpmath.mpf:
    with mpmath.workdps(precision):
        return _mp_fraction(f7_arithmetic_renormalization(b)) * evaluate_tilde_f7(b, precision=precision)


@lru_cache(maxsize=None)
def extract_f7_linear_form(b: tuple[int, ...]) -> ExactDualF7LinearForm:
    _validate_b_vector(b)
    normalization_numerator_factorials, normalization_denominator_factorials = _f7_arithmetic_renormalization_factorials(b)
    denominator_exponents, _, central_shift = _build_reduced_factor_data(b)
    shift_intervals = _build_shift_intervals(b)
    constant_numerator = 0
    constant_denominator = 1
    zeta_components_by_weight: dict[int, tuple[int, int]] = {}
    for shift, order in denominator_exponents.items():
        regular_series_components = _pole_regular_series_components(
            shift=shift,
            order=order,
            normalization_numerator_factorials=normalization_numerator_factorials,
            normalization_denominator_factorials=normalization_denominator_factorials,
            max_shift=b[0] + 1,
            shift_intervals=shift_intervals,
            central_shift=central_shift,
        )
        for weight in range(1, order + 1):
            coefficient_numerator, coefficient_denominator = regular_series_components[order - weight]
            if coefficient_numerator == 0:
                continue
            current_zeta_numerator, current_zeta_denominator = zeta_components_by_weight.get(weight, (0, 1))
            updated_zeta_numerator, updated_zeta_denominator = _add_fraction_components(
                left_numerator=current_zeta_numerator,
                left_denominator=current_zeta_denominator,
                right_numerator=coefficient_numerator,
                right_denominator=coefficient_denominator,
            )
            zeta_components_by_weight[weight] = (
                updated_zeta_numerator,
                updated_zeta_denominator,
            )
            harmonic_numerator, harmonic_denominator = _harmonic_number_raw_pair(shift - 1, weight)
            if harmonic_numerator:
                term_numerator, term_denominator = _multiply_fraction_components(
                    -coefficient_numerator,
                    coefficient_denominator,
                    harmonic_numerator,
                    harmonic_denominator,
                )
                constant_numerator, constant_denominator = _add_fraction_components(
                    left_numerator=constant_numerator,
                    left_denominator=constant_denominator,
                    right_numerator=term_numerator,
                    right_denominator=term_denominator,
                )

    constant_term = Fraction(
        constant_numerator,
        constant_denominator,
        _normalize=False,
    )
    zeta_coefficients = {
        weight: Fraction(numerator, denominator, _normalize=False)
        for weight, (numerator, denominator) in zeta_components_by_weight.items()
    }

    zeta_coefficients = {weight: coefficient for weight, coefficient in zeta_coefficients.items() if coefficient}
    linear_coefficient = zeta_coefficients.get(1, Fraction(0))
    if linear_coefficient:
        raise ValueError(f"extracted a nonzero zeta(1) coefficient: {fraction_to_canonical_string(linear_coefficient)}")

    return ExactDualF7LinearForm(
        b=b,
        constant_term=constant_term,
        zeta_coefficients=tuple(sorted(zeta_coefficients.items())),
    )


def evaluate_exact_f7_linear_form(
    linear_form: ExactDualF7LinearForm,
    *,
    precision: int = 120,
) -> mpmath.mpf:
    if precision < 40:
        raise ValueError("precision must be at least 40 decimal digits")
    with mpmath.workdps(precision):
        value = _mp_fraction(linear_form.constant_term)
        for weight, coefficient in linear_form.zeta_coefficients:
            value += _mp_fraction(coefficient) * mpmath.zeta(weight)
        return value


def search_f7_zeta_relation(
    value: mpmath.mpf,
    *,
    precision: int = 180,
    maxcoeff: int = 100000,
) -> DualF7Relation | None:
    if precision < 80:
        raise ValueError("precision must be at least 80 decimal digits")
    if maxcoeff <= 0:
        raise ValueError("maxcoeff must be positive")
    with mpmath.workdps(precision):
        if not value:
            return None
        vector = [mpmath.mpf(1), mpmath.zeta(3), mpmath.zeta(5), value]
        tolerance_power = max(20, min(precision // 2, 100))
        tolerance = mpmath.mpf(10) ** (-tolerance_power)
        try:
            relation = mpmath.pslq(vector, maxcoeff=maxcoeff, tol=tolerance)
        except ValueError:
            return None
        if relation is None:
            return None
        coefficients = _normalize_integer_relation(tuple(int(entry) for entry in relation))
        if coefficients[3] == 0:
            return None
        residual = abs(
            coefficients[0]
            + coefficients[1] * mpmath.zeta(3)
            + coefficients[2] * mpmath.zeta(5)
            + coefficients[3] * value
        )
        residual_log10_abs = None if residual == 0 else float(mpmath.log10(residual))
    c0, c1, c2, c3 = coefficients
    return DualF7Relation(
        coefficients=coefficients,
        constant_term=Fraction(-c0, c3),
        zeta3_coeff=Fraction(-c1, c3),
        zeta5_coeff=Fraction(-c2, c3),
        residual_log10_abs=residual_log10_abs,
    )


def render_dual_f7_relation(relation: DualF7Relation) -> str:
    pieces = [fraction_to_canonical_string(relation.constant_term)]
    pieces.append(_format_signed_linear_term(relation.zeta3_coeff, "zeta(3)"))
    pieces.append(_format_signed_linear_term(relation.zeta5_coeff, "zeta(5)"))
    return "F_7 = " + " ".join(pieces)


def render_exact_f7_linear_form(linear_form: ExactDualF7LinearForm) -> str:
    pieces = [fraction_to_canonical_string(linear_form.constant_term)]
    for weight, coefficient in linear_form.zeta_coefficients:
        pieces.append(_format_signed_linear_term(coefficient, f"zeta({weight})"))
    return "F_7 = " + " ".join(pieces)


def displayed_series_to_hyper_line_ratio(b: tuple[int, ...]) -> int:
    _validate_b_vector(b)
    return b[0] + 2


def extract_f7_zeta5_coefficient(b: tuple[int, ...]) -> int:
    _validate_b_vector(b)
    normalization = f7_arithmetic_renormalization(b)
    denominator_exponents, leftover_integer_factors, central_shift = _build_reduced_factor_data(b)
    total = Fraction(0)
    for shift, order in denominator_exponents.items():
        if order < 5:
            continue
        numerator_value = normalization
        numerator_log_derivative = Fraction(0)
        for factor_shift, exponent in leftover_integer_factors.items():
            delta = factor_shift - shift
            numerator_value *= delta**exponent
            numerator_log_derivative += Fraction(exponent, delta)

        if central_shift is None:
            linear_delta = b[0] + 2 - 2 * shift
            numerator_value *= linear_delta
            numerator_log_derivative += Fraction(2, linear_delta)
        else:
            # When the central shift is integral, the displayed linear factor contributes
            # one global constant factor 2 after canceling a single pole at that shift.
            numerator_value *= 2

        denominator_value = 1
        denominator_log_derivative = Fraction(0)
        for factor_shift, exponent in denominator_exponents.items():
            if factor_shift == shift:
                continue
            delta = factor_shift - shift
            denominator_value *= delta**exponent
            denominator_log_derivative += Fraction(exponent, delta)

        leading_coefficient = Fraction(numerator_value, denominator_value)
        if order == 5:
            total += leading_coefficient
        elif order == 6:
            total += leading_coefficient * (numerator_log_derivative - denominator_log_derivative)
        else:
            raise ValueError(f"unexpected reduced pole order {order}; zeta(5) extractor expects order at most 6")

    if total.denominator != 1:
        raise ValueError(f"expected an integral zeta(5) coefficient, found {fraction_to_canonical_string(total)}")
    return total.numerator


def _validate_b_vector(b: tuple[int, ...]) -> None:
    if len(b) != 8:
        raise ValueError("b must have length 8")
    b0, *tail = b
    if b0 < 0 or any(value < 0 for value in tail):
        raise ValueError("b entries must be nonnegative")
    if any(b0 < 2 * value for value in tail):
        raise ValueError("b0 must satisfy b0 >= 2*b_i for i>=1")


def _normalize_integer_relation(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    divisor = reduce(gcd, (abs(value) for value in coefficients if value))
    normalized = tuple(value // divisor for value in coefficients)
    for value in normalized:
        if value < 0:
            return tuple(-entry for entry in normalized)
        if value > 0:
            return normalized
    return normalized


def _mp_fraction(value: Fraction) -> mpmath.mpf:
    return mpmath.mpf(value.numerator) / value.denominator


def _format_signed_linear_term(coefficient: Fraction, basis_label: str) -> str:
    sign = "+" if coefficient >= 0 else "-"
    magnitude = fraction_to_canonical_string(abs(coefficient))
    return f"{sign} {magnitude}*{basis_label}"


def _normalize_component_label(component: str) -> str:
    normalized = component.strip().lower().replace("(", "").replace(")", "").replace("_", "")
    if normalized in {"constant", "c0"}:
        return "constant"
    if normalized in {"zeta3", "ζ3"}:
        return "zeta3"
    if normalized in {"zeta5", "ζ5"}:
        return "zeta5"
    raise ValueError(f"unsupported dual F_7 exact component {component!r}")


def _build_reduced_factor_data(b: tuple[int, ...]) -> tuple[dict[int, int], dict[int, int], int | None]:
    raw_counts = _build_raw_denominator_counts(b)
    denominator_exponents: dict[int, int] = {}
    leftover_integer_factors: dict[int, int] = {}
    central_shift = (b[0] + 2) // 2 if b[0] % 2 == 0 else None

    for shift in range(1, b[0] + 2):
        order = raw_counts.get(shift, 0) - 1
        if central_shift is not None and shift == central_shift:
            order -= 1
        if order > 0:
            denominator_exponents[shift] = order
        elif raw_counts.get(shift, 0) == 0:
            leftover_integer_factors[shift] = 1

    return denominator_exponents, leftover_integer_factors, central_shift


def _build_raw_denominator_counts(b: tuple[int, ...]) -> dict[int, int]:
    counts: dict[int, int] = {}
    b0, *tail = b
    for value in tail:
        for shift in range(value + 1, b0 - value + 2):
            counts[shift] = counts.get(shift, 0) + 1
    return counts


def _extract_linear_pole_coefficients(b: tuple[int, ...]) -> dict[int, dict[int, Fraction]]:
    normalization_numerator_factorials, normalization_denominator_factorials = _f7_arithmetic_renormalization_factorials(b)
    denominator_exponents, _, central_shift = _build_reduced_factor_data(b)
    shift_intervals = _build_shift_intervals(b)
    pole_coefficients: dict[int, dict[int, Fraction]] = {}
    for shift, order in denominator_exponents.items():
        regular_series = _pole_regular_series(
            shift=shift,
            order=order,
            normalization_numerator_factorials=normalization_numerator_factorials,
            normalization_denominator_factorials=normalization_denominator_factorials,
            max_shift=b[0] + 1,
            shift_intervals=shift_intervals,
            central_shift=central_shift,
        )
        pole_coefficients[shift] = {
            weight: regular_series[order - weight]
            for weight in range(1, order + 1)
            if regular_series[order - weight] != 0
        }
    return pole_coefficients


def _pole_regular_series(
    *,
    shift: int,
    order: int,
    normalization_numerator_factorials: tuple[int, ...],
    normalization_denominator_factorials: tuple[int, ...],
    max_shift: int,
    shift_intervals: tuple[tuple[int, int], ...],
    central_shift: int | None,
) -> tuple[Fraction, ...]:
    return tuple(
        Fraction(numerator, denominator, _normalize=False)
        for numerator, denominator in _pole_regular_series_components(
            shift=shift,
            order=order,
            normalization_numerator_factorials=normalization_numerator_factorials,
            normalization_denominator_factorials=normalization_denominator_factorials,
            max_shift=max_shift,
            shift_intervals=shift_intervals,
            central_shift=central_shift,
        )
    )


def _pole_regular_series_components(
    *,
    shift: int,
    order: int,
    normalization_numerator_factorials: tuple[int, ...],
    normalization_denominator_factorials: tuple[int, ...],
    max_shift: int,
    shift_intervals: tuple[tuple[int, int], ...],
    central_shift: int | None,
) -> tuple[tuple[int, int], ...]:
    truncated_degree = order - 1
    log_terms_by_degree: list[list[tuple[int, int]]] = [[] for _ in range(truncated_degree + 1)]

    for degree in range(1, truncated_degree + 1):
        reciprocal_sum = _all_shift_reciprocal_power_sum(max_shift=max_shift, shift=shift, degree=degree)
        scaled_numerator, scaled_denominator = _scaled_reciprocal_sum_components(
            numerator=(((-1) ** (degree + 1)) * reciprocal_sum.numerator),
            denominator=reciprocal_sum.denominator,
            scale=degree,
        )
        log_terms_by_degree[degree].append((scaled_numerator, scaled_denominator))

    if central_shift is None:
        linear_delta = max_shift + 1 - 2 * shift
        _append_log_linear_power_terms_to_term_lists(
            terms_by_degree=log_terms_by_degree,
            delta=linear_delta,
            slope=2,
            exponent=1,
            truncated_degree=truncated_degree,
        )
    else:
        if central_shift != shift:
            central_delta = central_shift - shift
            _append_log_linear_power_terms_to_term_lists(
                terms_by_degree=log_terms_by_degree,
                delta=central_delta,
                slope=1,
                exponent=1,
                truncated_degree=truncated_degree,
            )
    for left, right in shift_intervals:
        for degree in range(1, truncated_degree + 1):
            reciprocal_sum = _interval_reciprocal_power_sum(left=left, right=right, shift=shift, degree=degree)
            scaled_numerator, scaled_denominator = _scaled_reciprocal_sum_components(
                numerator=(((-1) ** degree) * reciprocal_sum.numerator),
                denominator=reciprocal_sum.denominator,
                scale=degree,
            )
            log_terms_by_degree[degree].append((scaled_numerator, scaled_denominator))

    log_numerators = [0 for _ in range(truncated_degree + 1)]
    log_denominators = [1 for _ in range(truncated_degree + 1)]
    for degree in range(1, truncated_degree + 1):
        log_numerators[degree], log_denominators[degree] = _sum_fraction_component_terms(log_terms_by_degree[degree])

    constant = _pole_constant_factorization(
        shift=shift,
        normalization_numerator_factorials=normalization_numerator_factorials,
        normalization_denominator_factorials=normalization_denominator_factorials,
        max_shift=max_shift,
        shift_intervals=shift_intervals,
        central_shift=central_shift,
    )
    exponential_series = _exp_truncated_series_from_log_components(
        numerators=tuple(log_numerators),
        denominators=tuple(log_denominators),
    )
    result_coefficients: list[tuple[int, int]] = []
    for numerator, denominator in exponential_series:
        result_coefficients.append(
            _multiply_factorized_rational_components(
                constant,
                numerator=numerator,
                denominator=denominator,
            )
        )
    return tuple(result_coefficients)


def _build_shift_intervals(b: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    b0, *tail = b
    return tuple((value + 1, b0 - value + 1) for value in tail)


@lru_cache(maxsize=None)
def _all_shift_reciprocal_power_sum(*, max_shift: int, shift: int, degree: int) -> Fraction:
    return _combine_harmonic_number_limits(
        left_limit=shift - 1,
        right_limit=max_shift - shift,
        weight=degree,
        left_sign=-1 if degree % 2 else 1,
    )


@lru_cache(maxsize=None)
def _interval_reciprocal_power_sum(*, left: int, right: int, shift: int, degree: int) -> Fraction:
    if shift < left:
        return _combine_harmonic_number_limits(
            left_limit=right - shift,
            right_limit=left - shift - 1,
            weight=degree,
            right_sign=-1,
        )
    if shift > right:
        sign = -1 if degree % 2 else 1
        return _combine_harmonic_number_limits(
            left_limit=shift - left,
            right_limit=shift - right - 1,
            weight=degree,
            left_sign=sign,
            right_sign=-sign,
        )
    return _combine_harmonic_number_limits(
        left_limit=shift - left,
        right_limit=right - shift,
        weight=degree,
        left_sign=-1 if degree % 2 else 1,
    )


def _accumulate_reduced_fraction(
    *,
    numerators: list[int],
    denominators: list[int],
    degree: int,
    numerator: int,
    denominator: int,
) -> None:
    if numerator == 0:
        return
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    current_numerator = numerators[degree]
    current_denominator = denominators[degree]
    if current_numerator == 0:
        if max(abs(numerator).bit_length(), denominator.bit_length()) >= _FINAL_SUM_NORMALIZATION_GCD_BIT_LENGTH_CUTOFF:
            numerators[degree] = numerator
            denominators[degree] = denominator
            return
        divisor = gcd(abs(numerator), denominator)
        numerators[degree] = numerator // divisor
        denominators[degree] = denominator // divisor
        return
    if gmpy2 is not None:
        magnitude_bit_length = max(
            abs(current_numerator).bit_length(),
            current_denominator.bit_length(),
            abs(numerator).bit_length(),
            denominator.bit_length(),
        )
        if magnitude_bit_length >= _RATIONAL_BACKEND_ADDITION_BIT_LENGTH_CUTOFF:
            updated_numerator, updated_denominator = _add_fraction_components(
                left_numerator=current_numerator,
                left_denominator=current_denominator,
                right_numerator=numerator,
                right_denominator=denominator,
            )
            numerators[degree] = updated_numerator
            denominators[degree] = updated_denominator
            return

    common_divisor = gcd(current_denominator, denominator)
    if common_divisor == 1:
        numerators[degree] = current_numerator * denominator + numerator * current_denominator
        denominators[degree] = current_denominator * denominator
        return

    scaled_current_denominator = current_denominator // common_divisor
    combined_numerator = current_numerator * (denominator // common_divisor) + numerator * scaled_current_denominator
    shared_divisor = gcd(abs(combined_numerator), common_divisor)
    numerators[degree] = combined_numerator // shared_divisor
    denominators[degree] = scaled_current_denominator * (denominator // shared_divisor)


def _append_log_linear_power_terms(
    *,
    terms_by_degree: list[list[Fraction]],
    delta: int,
    slope: int,
    exponent: int,
    truncated_degree: int,
) -> None:
    if exponent == 0 or truncated_degree <= 0:
        return
    for degree in range(1, truncated_degree + 1):
        terms_by_degree[degree].append(
            _scaled_reciprocal_sum_term(
                numerator=exponent * ((-1) ** (degree + 1)) * (slope**degree),
                denominator=delta**degree,
                scale=degree,
            )
        )


def _append_log_linear_power_terms_to_accumulator(
    *,
    numerators: list[int],
    denominators: list[int],
    delta: int,
    slope: int,
    exponent: int,
    truncated_degree: int,
) -> None:
    if exponent == 0 or truncated_degree <= 0:
        return
    for degree in range(1, truncated_degree + 1):
        scaled_numerator, scaled_denominator = _scaled_reciprocal_sum_components(
            numerator=exponent * ((-1) ** (degree + 1)) * (slope**degree),
            denominator=delta**degree,
            scale=degree,
        )
        _accumulate_reduced_fraction(
            numerators=numerators,
            denominators=denominators,
            degree=degree,
            numerator=scaled_numerator,
            denominator=scaled_denominator,
        )


def _append_log_linear_power_terms_to_term_lists(
    *,
    terms_by_degree: list[list[tuple[int, int]]],
    delta: int,
    slope: int,
    exponent: int,
    truncated_degree: int,
) -> None:
    if exponent == 0 or truncated_degree <= 0:
        return
    for degree in range(1, truncated_degree + 1):
        terms_by_degree[degree].append(
            _scaled_reciprocal_sum_components(
                numerator=exponent * ((-1) ** (degree + 1)) * (slope**degree),
                denominator=delta**degree,
                scale=degree,
            )
        )


def _sum_fraction_component_terms(terms: list[tuple[int, int]]) -> tuple[int, int]:
    if not terms:
        return 0, 1
    numerators_by_denominator: dict[int, int] = {}
    for numerator, denominator in terms:
        if numerator == 0:
            continue
        numerators_by_denominator[denominator] = numerators_by_denominator.get(denominator, 0) + numerator
    if not numerators_by_denominator:
        return 0, 1
    ordered_terms = sorted(
        (
            (numerator, denominator)
            for denominator, numerator in numerators_by_denominator.items()
            if numerator
        ),
        key=lambda item: (item[1].bit_length(), item[1]),
    )
    if (
        gmpy2 is not None
        and ordered_terms
        and ordered_terms[-1][1].bit_length() >= _MPQ_COMPONENT_SUM_DENOMINATOR_BIT_LENGTH_CUTOFF
    ):
        return _sum_fraction_component_terms_via_mpq(ordered_terms)
    total_numerator, total_denominator = ordered_terms[0]
    for numerator, denominator in ordered_terms[1:]:
        total_numerator, total_denominator = _add_fraction_components(
            left_numerator=total_numerator,
            left_denominator=total_denominator,
            right_numerator=numerator,
            right_denominator=denominator,
        )
    return total_numerator, total_denominator


def _sum_fraction_component_terms_via_mpq(terms: list[tuple[int, int]]) -> tuple[int, int]:
    if gmpy2 is None:  # pragma: no cover - guarded by caller
        raise RuntimeError("backend component sum path requires gmpy2")
    active_terms = [
        _fraction_pair_to_mpq(numerator, denominator)
        for numerator, denominator in terms
    ]
    while len(active_terms) > 1:
        active_terms.sort(
            key=lambda term: (
                gmpy2.denom(term).bit_length(),
                int(gmpy2.denom(term)),
            )
        )
        next_terms = []
        term_count = len(active_terms)
        index = 0
        while index + 1 < term_count:
            next_terms.append(active_terms[index] + active_terms[index + 1])
            index += 2
        if index < term_count:
            next_terms.append(active_terms[index])
        active_terms = next_terms
    result = active_terms[0]
    return int(gmpy2.numer(result)), int(gmpy2.denom(result))


def _exp_truncated_series_from_log_coefficients(
    log_coefficients: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    if gmpy2 is not None:
        max_magnitude_bit_length = 0
        for coefficient in log_coefficients[1:]:
            if coefficient:
                max_magnitude_bit_length = max(
                    max_magnitude_bit_length,
                    abs(coefficient.numerator).bit_length(),
                    coefficient.denominator.bit_length(),
                )
        if max_magnitude_bit_length >= _MPQ_EXP_SERIES_BIT_LENGTH_CUTOFF:
            return _exp_truncated_series_from_log_coefficients_via_mpq(log_coefficients)
    truncated_degree = len(log_coefficients) - 1
    coefficients = [Fraction(0) for _ in range(truncated_degree + 1)]
    coefficients[0] = Fraction(1)
    for degree in range(1, truncated_degree + 1):
        terms = []
        for offset in range(1, degree + 1):
            terms.append(
                _multiply_fraction_pair(
                    _scale_fraction(log_coefficients[offset], offset),
                    coefficients[degree - offset],
                )
            )
        coefficients[degree] = _sum_fraction_terms(tuple(terms)) / degree
    return tuple(coefficients)


def _exp_truncated_series_from_log_components(
    *,
    numerators: tuple[int, ...],
    denominators: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    truncated_degree = len(numerators) - 1
    coefficients: list[tuple[int, int]] = [(0, 1) for _ in range(truncated_degree + 1)]
    coefficients[0] = (1, 1)
    scaled_log_coefficients = [
        _scale_fraction_components(numerator, denominator, offset)
        for offset, (numerator, denominator) in enumerate(zip(numerators, denominators, strict=True))
    ]
    for degree in range(1, truncated_degree + 1):
        terms: list[tuple[int, int]] = []
        for offset in range(1, degree + 1):
            term_numerator, term_denominator = _multiply_fraction_components(
                *scaled_log_coefficients[offset],
                *coefficients[degree - offset],
            )
            if term_numerator:
                terms.append((term_numerator, term_denominator))
        total_numerator, total_denominator = _sum_fraction_component_terms(terms)
        coefficients[degree] = _divide_fraction_components_by_int(
            numerator=total_numerator,
            denominator=total_denominator,
            divisor=degree,
        )
    return tuple(coefficients)


def _exp_truncated_series_from_log_coefficients_via_mpq(
    log_coefficients: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    if gmpy2 is None:  # pragma: no cover - guarded by caller
        raise RuntimeError("mpq exp-series path requires gmpy2")
    truncated_degree = len(log_coefficients) - 1
    coefficients: list[tuple[int, int]] = [(0, 1) for _ in range(truncated_degree + 1)]
    coefficients[0] = (1, 1)
    scaled_log_coefficients = [
        _scale_fraction_components(value.numerator, value.denominator, offset)
        for offset, value in enumerate(log_coefficients)
    ]
    for degree in range(1, truncated_degree + 1):
        total_numerator = 0
        total_denominator = 1
        for offset in range(1, degree + 1):
            term_numerator, term_denominator = _multiply_fraction_components(
                *scaled_log_coefficients[offset],
                *coefficients[degree - offset],
            )
            total_numerator, total_denominator = _add_fraction_components(
                left_numerator=total_numerator,
                left_denominator=total_denominator,
                right_numerator=term_numerator,
                right_denominator=term_denominator,
            )
        coefficients[degree] = _divide_fraction_components_by_int(
            numerator=total_numerator,
            denominator=total_denominator,
            divisor=degree,
        )
    return tuple(
        Fraction(numerator, denominator, _normalize=False)
        for numerator, denominator in coefficients
    )


def _scale_fraction_components(numerator: int, denominator: int, scale: int) -> tuple[int, int]:
    if scale == 0 or numerator == 0:
        return 0, 1
    if scale == 1:
        return numerator, denominator
    common_divisor = gcd(scale, denominator)
    if common_divisor != 1:
        scale //= common_divisor
        denominator //= common_divisor
    return _exact_integer_product(numerator, scale), denominator


def _divide_fraction_components_by_int(*, numerator: int, denominator: int, divisor: int) -> tuple[int, int]:
    if numerator == 0:
        return 0, 1
    common_divisor = gcd(abs(numerator), divisor)
    if common_divisor != 1:
        numerator //= common_divisor
        divisor //= common_divisor
    if divisor != 1:
        denominator = _cached_exact_product(denominator, divisor)
    return numerator, denominator


def _fraction_pair_to_mpq(numerator: int, denominator: int):
    if max(abs(numerator).bit_length(), denominator.bit_length()) >= _MPQ_CONVERSION_CACHE_BIT_LENGTH_CUTOFF:
        return _fraction_pair_to_mpq_uncached(numerator, denominator)
    return _cached_fraction_pair_to_mpq(numerator, denominator)


@lru_cache(maxsize=None)
def _cached_fraction_pair_to_mpq(numerator: int, denominator: int):
    return _fraction_pair_to_mpq_uncached(numerator, denominator)


def _fraction_pair_to_mpq_uncached(numerator: int, denominator: int):
    if gmpy2 is None:  # pragma: no cover - guarded by caller
        raise RuntimeError("mpq conversion requires gmpy2")
    if numerator == 0:
        return gmpy2.mpq(0)
    if denominator == 1:
        return gmpy2.mpq(numerator)
    if numerator == denominator:
        return gmpy2.mpq(1)
    if numerator == -denominator:
        return gmpy2.mpq(-1)
    return gmpy2.mpq(numerator, denominator)


def _fraction_to_mpq(value: Fraction):
    return _fraction_pair_to_mpq(value.numerator, value.denominator)


def _sum_fraction_terms(terms: tuple[Fraction, ...]) -> Fraction:
    numerators_by_denominator: dict[int, int] = {}
    for term in terms:
        if not term:
            continue
        numerators_by_denominator[term.denominator] = numerators_by_denominator.get(term.denominator, 0) + term.numerator

    active_terms = [
        Fraction(numerator, denominator, _normalize=False)
        for denominator, numerator in numerators_by_denominator.items()
        if numerator
    ]
    if not active_terms:
        return Fraction(0)
    if gmpy2 is not None and max(term.denominator.bit_length() for term in active_terms) >= _MPQ_SUM_DENOMINATOR_BIT_LENGTH_CUTOFF:
        return _sum_fraction_terms_via_mpq(active_terms)
    while len(active_terms) > 1:
        active_terms.sort(
            key=lambda term: (
                term.denominator.bit_length(),
                term.denominator,
            )
        )
        next_terms: list[Fraction] = []
        term_count = len(active_terms)
        index = 0
        while index + 1 < term_count:
            next_terms.append(_add_fraction_pair(active_terms[index], active_terms[index + 1]))
            index += 2
        if index < term_count:
            next_terms.append(active_terms[index])
        active_terms = next_terms
    result = active_terms[0]
    if max(abs(result.numerator).bit_length(), result.denominator.bit_length()) >= _FINAL_SUM_NORMALIZATION_GCD_BIT_LENGTH_CUTOFF:
        return result
    reduction_divisor = gcd(abs(result.numerator), result.denominator)
    if reduction_divisor == 1:
        return result
    return Fraction(
        result.numerator // reduction_divisor,
        result.denominator // reduction_divisor,
        _normalize=False,
    )


def _sum_fraction_terms_via_mpq(terms: list[Fraction]) -> Fraction:
    active_terms = [
        (term.numerator, term.denominator)
        for term in terms
    ]
    while len(active_terms) > 1:
        active_terms.sort(
            key=lambda term: (
                term[1].bit_length(),
                term[1],
            )
        )
        next_terms: list[tuple[int, int]] = []
        term_count = len(active_terms)
        index = 0
        while index + 1 < term_count:
            left_numerator, left_denominator = active_terms[index]
            right_numerator, right_denominator = active_terms[index + 1]
            next_terms.append(
                _add_fraction_components(
                    left_numerator=left_numerator,
                    left_denominator=left_denominator,
                    right_numerator=right_numerator,
                    right_denominator=right_denominator,
                )
            )
            index += 2
        if index < term_count:
            next_terms.append(active_terms[index])
        active_terms = next_terms
    result_numerator, result_denominator = active_terms[0]
    return Fraction(result_numerator, result_denominator, _normalize=False)


def _select_fraction_pair_indices(active_terms: list[Fraction]) -> tuple[int, int]:
    ordered_indices = sorted(
        range(len(active_terms)),
        key=lambda index: (
            active_terms[index].denominator.bit_length(),
            active_terms[index].denominator,
        ),
    )
    best_left_index = ordered_indices[0]
    best_right_index = ordered_indices[1]
    best_key = _fraction_pair_key(active_terms[best_left_index], active_terms[best_right_index])
    active_count = len(ordered_indices)
    for ordered_left_index in range(active_count - 1):
        left_index = ordered_indices[ordered_left_index]
        left = active_terms[left_index]
        right_limit = min(active_count, ordered_left_index + 1 + _FRACTION_PAIR_SELECTION_WINDOW)
        for ordered_right_index in range(ordered_left_index + 1, right_limit):
            right_index = ordered_indices[ordered_right_index]
            pair_key = _fraction_pair_key(left, active_terms[right_index])
            if pair_key > best_key:
                best_left_index = left_index
                best_right_index = right_index
                best_key = pair_key
    if best_left_index > best_right_index:
        best_left_index, best_right_index = best_right_index, best_left_index
    return best_left_index, best_right_index


def _fraction_pair_key(left: Fraction, right: Fraction) -> tuple[int, int, int]:
    left_bit_length = left.denominator.bit_length()
    right_bit_length = right.denominator.bit_length()
    return (
        -max(left_bit_length, right_bit_length),
        -(left_bit_length + right_bit_length),
        -abs(left_bit_length - right_bit_length),
    )


def _add_fraction_pair(left: Fraction, right: Fraction) -> Fraction:
    if left == 0:
        return right
    if right == 0:
        return left
    if gmpy2 is not None:
        magnitude_bit_length = max(
            abs(left.numerator).bit_length(),
            left.denominator.bit_length(),
            abs(right.numerator).bit_length(),
            right.denominator.bit_length(),
        )
        if magnitude_bit_length >= _RATIONAL_BACKEND_ADDITION_BIT_LENGTH_CUTOFF:
            return _add_fraction_pair_via_backend(left, right)
    left_numerator, left_denominator = left.numerator, left.denominator
    right_numerator, right_denominator = right.numerator, right.denominator
    common_divisor = _cached_pair_gcd(left_denominator, right_denominator)
    if common_divisor == 1:
        combined_numerator = _combine_scaled_numerators(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_denominator,
            right_scale=right_denominator,
        )
        if combined_numerator == 0:
            return Fraction(0)
        return _reduced_fraction_from_factor_pair(
            combined_numerator=combined_numerator,
            left_denominator_factor=left_denominator,
            right_denominator_factor=right_denominator,
        )
    if max(left_denominator.bit_length(), right_denominator.bit_length(), common_divisor.bit_length()) >= _ADDITION_QUOTIENT_BIT_LENGTH_CUTOFF:
        combined_numerator = _combine_scaled_numerators(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_denominator,
            right_scale=right_denominator,
        )
        if combined_numerator == 0:
            return Fraction(0)
        return _reduced_fraction_from_factor_pair(
            combined_numerator=combined_numerator,
            left_denominator_factor=left_denominator,
            right_denominator_factor=right_denominator,
        )
    if common_divisor == left_denominator:
        left_scale = 1
    else:
        left_scale = _cached_exact_quotient(left_denominator, common_divisor)
    if common_divisor == right_denominator:
        right_scale = 1
    else:
        right_scale = _cached_exact_quotient(right_denominator, common_divisor)
    combined_numerator = _combine_scaled_numerators(
        left_numerator=left_numerator,
        right_numerator=right_numerator,
        left_scale=left_scale,
        right_scale=right_scale,
    )
    if combined_numerator == 0:
        return Fraction(0)
    return _reduced_fraction_from_factor_pair(
        combined_numerator=combined_numerator,
        left_denominator_factor=left_scale,
        right_denominator_factor=right_denominator,
    )


def _add_fraction_components(
    *,
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> tuple[int, int]:
    if left_numerator == 0:
        return right_numerator, right_denominator
    if right_numerator == 0:
        return left_numerator, left_denominator
    if gmpy2 is not None:
        magnitude_bit_length = max(
            abs(left_numerator).bit_length(),
            left_denominator.bit_length(),
            abs(right_numerator).bit_length(),
            right_denominator.bit_length(),
        )
        if magnitude_bit_length >= _RATIONAL_BACKEND_ADDITION_BIT_LENGTH_CUTOFF:
            return _add_fraction_components_via_backend(
                left_numerator=left_numerator,
                left_denominator=left_denominator,
                right_numerator=right_numerator,
                right_denominator=right_denominator,
            )
    common_divisor = _cached_pair_gcd(left_denominator, right_denominator)
    if common_divisor == 1:
        combined_numerator = _combine_scaled_numerators(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_denominator,
            right_scale=right_denominator,
        )
        if combined_numerator == 0:
            return 0, 1
        return _reduced_fraction_components_from_factor_pair(
            combined_numerator=combined_numerator,
            left_denominator_factor=left_denominator,
            right_denominator_factor=right_denominator,
        )
    if common_divisor == left_denominator:
        left_scale = 1
    else:
        left_scale = _known_exact_quotient(left_denominator, common_divisor)
    if common_divisor == right_denominator:
        right_scale = 1
    else:
        right_scale = _known_exact_quotient(right_denominator, common_divisor)
    combined_numerator = _combine_scaled_numerators(
        left_numerator=left_numerator,
        right_numerator=right_numerator,
        left_scale=left_scale,
        right_scale=right_scale,
    )
    if combined_numerator == 0:
        return 0, 1
    return _reduced_fraction_components_from_factor_pair(
        combined_numerator=combined_numerator,
        left_denominator_factor=left_scale,
        right_denominator_factor=right_denominator,
    )


def _add_fraction_components_via_backend(
    *,
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> tuple[int, int]:
    if gmpy2 is None:  # pragma: no cover - guarded by caller
        raise RuntimeError("backend component add path requires gmpy2")
    if left_denominator == right_denominator:
        combined_numerator = left_numerator + right_numerator
        if combined_numerator == 0:
            return 0, 1
        if max(abs(combined_numerator).bit_length(), left_denominator.bit_length()) >= _BACKEND_ADD_REDUCTION_GCD_BIT_LENGTH_CUTOFF:
            return combined_numerator, left_denominator
        common_divisor = _exact_gcd(abs(combined_numerator), left_denominator)
        if common_divisor == 1:
            return combined_numerator, left_denominator
        return _exact_quotient(combined_numerator, common_divisor), _exact_quotient(left_denominator, common_divisor)
    if left_denominator % right_denominator == 0:
        scale = _exact_quotient(left_denominator, right_denominator)
        combined_numerator = left_numerator + _signed_exact_product(right_numerator, scale)
        if combined_numerator == 0:
            return 0, 1
        if max(abs(combined_numerator).bit_length(), left_denominator.bit_length()) >= _BACKEND_ADD_REDUCTION_GCD_BIT_LENGTH_CUTOFF:
            return combined_numerator, left_denominator
        common_divisor = _exact_gcd(abs(combined_numerator), left_denominator)
        if common_divisor == 1:
            return combined_numerator, left_denominator
        return _exact_quotient(combined_numerator, common_divisor), _exact_quotient(left_denominator, common_divisor)
    if right_denominator % left_denominator == 0:
        scale = _exact_quotient(right_denominator, left_denominator)
        combined_numerator = _signed_exact_product(left_numerator, scale) + right_numerator
        if combined_numerator == 0:
            return 0, 1
        if max(abs(combined_numerator).bit_length(), right_denominator.bit_length()) >= _BACKEND_ADD_REDUCTION_GCD_BIT_LENGTH_CUTOFF:
            return combined_numerator, right_denominator
        common_divisor = _exact_gcd(abs(combined_numerator), right_denominator)
        if common_divisor == 1:
            return combined_numerator, right_denominator
        return _exact_quotient(combined_numerator, common_divisor), _exact_quotient(right_denominator, common_divisor)
    if max(left_denominator.bit_length(), right_denominator.bit_length()) >= _BACKEND_ADD_REDUCTION_GCD_BIT_LENGTH_CUTOFF:
        combined = _fraction_pair_to_mpq(left_numerator, left_denominator) + _fraction_pair_to_mpq(
            right_numerator, right_denominator
        )
        return int(gmpy2.numer(combined)), int(gmpy2.denom(combined))
    common_divisor = _exact_gcd(left_denominator, right_denominator)
    left_scale = _exact_quotient(left_denominator, common_divisor)
    right_scale = _exact_quotient(right_denominator, common_divisor)
    combined_numerator = _combine_scaled_numerators_direct(
        left_numerator=left_numerator,
        right_numerator=right_numerator,
        left_scale=left_scale,
        right_scale=right_scale,
    )
    if combined_numerator == 0:
        return 0, 1
    combined_denominator = _exact_integer_product(left_scale, right_denominator)
    if max(abs(combined_numerator).bit_length(), combined_denominator.bit_length()) >= _BACKEND_ADD_REDUCTION_GCD_BIT_LENGTH_CUTOFF:
        return combined_numerator, combined_denominator
    reduction_divisor = _exact_gcd(abs(combined_numerator), combined_denominator)
    if reduction_divisor == 1:
        return combined_numerator, combined_denominator
    return (
        _exact_quotient(combined_numerator, reduction_divisor),
        _exact_quotient(combined_denominator, reduction_divisor),
    )


def _known_exact_quotient(value: int, divisor: int) -> int:
    if divisor == 1:
        return value
    if divisor == value:
        return 1
    if max(value.bit_length(), divisor.bit_length()) >= _ADDITION_QUOTIENT_BIT_LENGTH_CUTOFF:
        return _exact_quotient(value, divisor)
    return _cached_exact_quotient(value, divisor)


def _add_fraction_pair_via_mpq(
    *,
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> Fraction:
    if gmpy2 is None:  # pragma: no cover - guarded by caller
        raise RuntimeError("mpq add path requires gmpy2")
    value = _fraction_pair_to_mpq(left_numerator, left_denominator) + _fraction_pair_to_mpq(
        right_numerator, right_denominator
    )
    return Fraction(int(gmpy2.numer(value)), int(gmpy2.denom(value)), _normalize=False)


def _multiply_fraction_pair_via_backend(left: Fraction, right: Fraction) -> Fraction:
    if gmpy2 is None:  # pragma: no cover - guarded by caller
        raise RuntimeError("backend multiply path requires gmpy2")
    value = gmpy2.mpq(left.numerator, left.denominator) * gmpy2.mpq(right.numerator, right.denominator)
    return Fraction(int(gmpy2.numer(value)), int(gmpy2.denom(value)), _normalize=False)


def _scale_fraction(value: Fraction, scale: int) -> Fraction:
    if scale == 0 or value == 0:
        return Fraction(0)
    if scale == 1:
        return value
    numerator, denominator = value.numerator, value.denominator
    common_divisor = gcd(scale, denominator)
    if common_divisor != 1:
        scale //= common_divisor
        denominator //= common_divisor
    return Fraction(numerator * scale, denominator, _normalize=False)


def _multiply_fraction_pair(left: Fraction, right: Fraction) -> Fraction:
    if left == 0 or right == 0:
        return Fraction(0)
    if gmpy2 is not None:
        magnitude_bit_length = max(
            abs(left.numerator).bit_length(),
            left.denominator.bit_length(),
            abs(right.numerator).bit_length(),
            right.denominator.bit_length(),
        )
        if magnitude_bit_length >= _BACKEND_MULTIPLICATION_BIT_LENGTH_CUTOFF:
            return _multiply_fraction_pair_via_backend(left, right)
    left_numerator, left_denominator = left.numerator, left.denominator
    right_numerator, right_denominator = right.numerator, right.denominator
    left_numerator_abs = abs(left_numerator)
    if left_numerator_abs == 1 or right_denominator == 1:
        left_reduction = 1
    elif left_numerator_abs == right_denominator:
        left_reduction = right_denominator
    elif max(left_numerator_abs.bit_length(), right_denominator.bit_length()) >= _MULTIPLICATION_GCD_BIT_LENGTH_CUTOFF:
        left_reduction = 1
    else:
        left_reduction = _cached_pair_gcd(left_numerator_abs, right_denominator)
    if left_reduction != 1:
        left_numerator //= left_reduction
        if left_reduction == right_denominator:
            right_denominator = 1
        else:
            right_denominator = _cached_exact_quotient(right_denominator, left_reduction)
    right_numerator_abs = abs(right_numerator)
    if right_numerator_abs == 1 or left_denominator == 1:
        right_reduction = 1
    elif right_numerator_abs == left_denominator:
        right_reduction = left_denominator
    elif max(right_numerator_abs.bit_length(), left_denominator.bit_length()) >= _MULTIPLICATION_GCD_BIT_LENGTH_CUTOFF:
        right_reduction = 1
    else:
        right_reduction = _cached_pair_gcd(right_numerator_abs, left_denominator)
    if right_reduction != 1:
        right_numerator //= right_reduction
        if right_reduction == left_denominator:
            left_denominator = 1
        else:
            left_denominator = _cached_exact_quotient(left_denominator, right_reduction)
    return Fraction(
        _exact_integer_product(left_numerator, right_numerator),
        _cached_exact_product(left_denominator, right_denominator),
        _normalize=False,
    )


def _multiply_fraction_components(
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> tuple[int, int]:
    if left_numerator == 0 or right_numerator == 0:
        return 0, 1
    left_numerator_abs = abs(left_numerator)
    if left_numerator_abs == 1 or right_denominator == 1:
        left_reduction = 1
    elif left_numerator_abs == right_denominator:
        left_reduction = right_denominator
    elif max(left_numerator_abs.bit_length(), right_denominator.bit_length()) >= _MULTIPLICATION_GCD_BIT_LENGTH_CUTOFF:
        left_reduction = 1
    else:
        left_reduction = _cached_pair_gcd(left_numerator_abs, right_denominator)
    if left_reduction != 1:
        left_numerator //= left_reduction
        if left_reduction == right_denominator:
            right_denominator = 1
        else:
            right_denominator = _cached_exact_quotient(right_denominator, left_reduction)
    right_numerator_abs = abs(right_numerator)
    if right_numerator_abs == 1 or left_denominator == 1:
        right_reduction = 1
    elif right_numerator_abs == left_denominator:
        right_reduction = left_denominator
    elif max(right_numerator_abs.bit_length(), left_denominator.bit_length()) >= _MULTIPLICATION_GCD_BIT_LENGTH_CUTOFF:
        right_reduction = 1
    else:
        right_reduction = _cached_pair_gcd(right_numerator_abs, left_denominator)
    if right_reduction != 1:
        right_numerator //= right_reduction
        if right_reduction == left_denominator:
            left_denominator = 1
        else:
            left_denominator = _cached_exact_quotient(left_denominator, right_reduction)
    return (
        _exact_integer_product(left_numerator, right_numerator),
        _cached_exact_product(left_denominator, right_denominator),
    )


def _combine_scaled_numerators(
    *,
    left_numerator: int,
    right_numerator: int,
    left_scale: int,
    right_scale: int,
) -> int:
    if left_scale == right_scale:
        return (left_numerator + right_numerator) * left_scale
    if left_scale == 1:
        return _signed_exact_product(left_numerator, right_scale) + right_numerator
    if right_scale == 1:
        return left_numerator + _signed_exact_product(right_numerator, left_scale)
    if abs(left_numerator) == 1:
        return _combine_scaled_numerators_direct(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_scale,
            right_scale=right_scale,
        )
    if abs(right_numerator) == 1:
        return _combine_scaled_numerators_direct(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_scale,
            right_scale=right_scale,
        )
    numerator_bit_length = max(abs(left_numerator).bit_length(), abs(right_numerator).bit_length())
    numerator_gcd_cutoff = (
        _NUMERATOR_GCD_BIT_LENGTH_CUTOFF_WITH_GMPY2 if gmpy2 is not None else _NUMERATOR_GCD_BIT_LENGTH_CUTOFF
    )
    if numerator_bit_length >= numerator_gcd_cutoff:
        return _combine_scaled_numerators_direct(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_scale,
            right_scale=right_scale,
        )
    common_numerator_divisor = _cached_pair_gcd(abs(left_numerator), abs(right_numerator))
    if common_numerator_divisor == 1:
        return _combine_scaled_numerators_direct(
            left_numerator=left_numerator,
            right_numerator=right_numerator,
            left_scale=left_scale,
            right_scale=right_scale,
        )
    return common_numerator_divisor * (
        (left_numerator // common_numerator_divisor) * right_scale
        + (right_numerator // common_numerator_divisor) * left_scale
    )


def _add_fraction_pair_via_backend(left: Fraction, right: Fraction) -> Fraction:
    combined = gmpy2.mpq(left.numerator, left.denominator) + gmpy2.mpq(right.numerator, right.denominator)
    return Fraction(int(combined.numerator), int(combined.denominator), _normalize=False)


def _combine_scaled_numerators_direct(
    *,
    left_numerator: int,
    right_numerator: int,
    left_scale: int,
    right_scale: int,
) -> int:
    if left_numerator == 1:
        return right_scale + _signed_exact_product(right_numerator, left_scale)
    if left_numerator == -1:
        return -right_scale + _signed_exact_product(right_numerator, left_scale)
    if right_numerator == 1:
        return _signed_exact_product(left_numerator, right_scale) + left_scale
    if right_numerator == -1:
        return _signed_exact_product(left_numerator, right_scale) - left_scale
    if gmpy2 is not None:
        if right_scale >= left_scale:
            return int(gmpy2.fma(gmpy2.mpz(left_numerator), right_scale, gmpy2.mpz(right_numerator) * left_scale))
        return int(gmpy2.fma(gmpy2.mpz(right_numerator), left_scale, gmpy2.mpz(left_numerator) * right_scale))
    return _signed_exact_product(left_numerator, right_scale) + _signed_exact_product(right_numerator, left_scale)


def _reduced_fraction_from_factor_pair(
    *,
    combined_numerator: int,
    left_denominator_factor: int,
    right_denominator_factor: int,
) -> Fraction:
    numerator_abs = abs(combined_numerator)
    if left_denominator_factor >= right_denominator_factor:
        first_factor = left_denominator_factor
        second_factor = right_denominator_factor
        first_is_left = True
    else:
        first_factor = right_denominator_factor
        second_factor = left_denominator_factor
        first_is_left = False

    if first_factor == 1 or numerator_abs == 1:
        first_reduction = 1
    elif first_factor == numerator_abs:
        first_reduction = first_factor
    elif max(first_factor.bit_length(), numerator_abs.bit_length()) >= _REDUCTION_GCD_BIT_LENGTH_CUTOFF:
        first_reduction = 1
    else:
        first_reduction = _cached_pair_gcd(first_factor, numerator_abs)
    remaining_numerator_abs = numerator_abs // first_reduction
    if second_factor == 1 or remaining_numerator_abs == 1:
        second_reduction = 1
    elif max(second_factor.bit_length(), remaining_numerator_abs.bit_length()) >= _REDUCTION_GCD_BIT_LENGTH_CUTOFF:
        second_reduction = 1
    else:
        second_reduction = _cached_pair_gcd(second_factor, remaining_numerator_abs)

    if first_reduction == 1 and second_reduction == 1:
        return _fraction_from_factor_pair(
            numerator=combined_numerator,
            left_factor=left_denominator_factor,
            right_factor=right_denominator_factor,
        )

    if first_is_left:
        left_reduction = first_reduction
        right_reduction = second_reduction
    else:
        left_reduction = second_reduction
        right_reduction = first_reduction
    if left_reduction == 1:
        left_quotient = left_denominator_factor
    elif left_reduction == left_denominator_factor:
        left_quotient = 1
    else:
        left_quotient = left_denominator_factor // left_reduction
    if right_reduction == 1:
        right_quotient = right_denominator_factor
    elif right_reduction == right_denominator_factor:
        right_quotient = 1
    else:
        right_quotient = right_denominator_factor // right_reduction

    if left_reduction >= right_reduction:
        first_numerator_reduction = left_reduction
        second_numerator_reduction = right_reduction
    else:
        first_numerator_reduction = right_reduction
        second_numerator_reduction = left_reduction
    reduced_numerator = combined_numerator
    if first_numerator_reduction != 1:
        reduced_numerator //= first_numerator_reduction
    if second_numerator_reduction != 1:
        reduced_numerator //= second_numerator_reduction
    if left_quotient == 1:
        reduced_denominator = right_quotient
    elif right_quotient == 1:
        reduced_denominator = left_quotient
    else:
        reduced_denominator = _exact_factor_pair_product(left_quotient, right_quotient)
    return Fraction(
        reduced_numerator,
        reduced_denominator,
        _normalize=False,
    )


def _reduced_fraction_components_from_factor_pair(
    *,
    combined_numerator: int,
    left_denominator_factor: int,
    right_denominator_factor: int,
) -> tuple[int, int]:
    numerator_abs = abs(combined_numerator)
    if left_denominator_factor >= right_denominator_factor:
        first_factor = left_denominator_factor
        second_factor = right_denominator_factor
        first_is_left = True
    else:
        first_factor = right_denominator_factor
        second_factor = left_denominator_factor
        first_is_left = False

    if first_factor == 1 or numerator_abs == 1:
        first_reduction = 1
    elif first_factor == numerator_abs:
        first_reduction = first_factor
    elif max(first_factor.bit_length(), numerator_abs.bit_length()) >= _REDUCTION_GCD_BIT_LENGTH_CUTOFF:
        first_reduction = 1
    else:
        first_reduction = _cached_pair_gcd(first_factor, numerator_abs)
    remaining_numerator_abs = numerator_abs // first_reduction
    if second_factor == 1 or remaining_numerator_abs == 1:
        second_reduction = 1
    elif max(second_factor.bit_length(), remaining_numerator_abs.bit_length()) >= _REDUCTION_GCD_BIT_LENGTH_CUTOFF:
        second_reduction = 1
    else:
        second_reduction = _cached_pair_gcd(second_factor, remaining_numerator_abs)

    if first_reduction == 1 and second_reduction == 1:
        return combined_numerator, _exact_factor_pair_product(left_denominator_factor, right_denominator_factor)

    if first_is_left:
        left_reduction = first_reduction
        right_reduction = second_reduction
    else:
        left_reduction = second_reduction
        right_reduction = first_reduction
    if left_reduction == 1:
        left_quotient = left_denominator_factor
    elif left_reduction == left_denominator_factor:
        left_quotient = 1
    else:
        left_quotient = left_denominator_factor // left_reduction
    if right_reduction == 1:
        right_quotient = right_denominator_factor
    elif right_reduction == right_denominator_factor:
        right_quotient = 1
    else:
        right_quotient = right_denominator_factor // right_reduction

    if left_reduction >= right_reduction:
        first_numerator_reduction = left_reduction
        second_numerator_reduction = right_reduction
    else:
        first_numerator_reduction = right_reduction
        second_numerator_reduction = left_reduction
    reduced_numerator = combined_numerator
    if first_numerator_reduction != 1:
        reduced_numerator //= first_numerator_reduction
    if second_numerator_reduction != 1:
        reduced_numerator //= second_numerator_reduction
    if left_quotient == 1:
        reduced_denominator = right_quotient
    elif right_quotient == 1:
        reduced_denominator = left_quotient
    else:
        reduced_denominator = _exact_factor_pair_product(left_quotient, right_quotient)
    return reduced_numerator, reduced_denominator


def _exact_factor_pair_product(left_factor: int, right_factor: int) -> int:
    if left_factor == 1:
        return right_factor
    if right_factor == 1:
        return left_factor
    if right_factor < left_factor:
        left_factor, right_factor = right_factor, left_factor
    if max(left_factor.bit_length(), right_factor.bit_length()) >= _FACTOR_PAIR_PRODUCT_CACHE_BIT_LENGTH_CUTOFF:
        if left_factor == right_factor:
            return _exact_product(left_factor, left_factor)
        if right_factor & (right_factor - 1) == 0:
            return left_factor << (right_factor.bit_length() - 1)
        return _exact_product(left_factor, right_factor)
    return _cached_exact_factor_pair_product(left_factor, right_factor)


@lru_cache(maxsize=None)
def _cached_exact_factor_pair_product(left_factor: int, right_factor: int) -> int:
    return _cached_exact_product(left_factor, right_factor)


def _fraction_from_factor_pair(*, numerator: int, left_factor: int, right_factor: int) -> Fraction:
    return Fraction(
        numerator,
        _exact_factor_pair_product(left_factor, right_factor),
        _normalize=False,
    )


def _negate_fraction(value: Fraction) -> Fraction:
    if value == 0:
        return Fraction(0)
    return Fraction(-value.numerator, value.denominator, _normalize=False)


def _signed_fraction(value: Fraction, *, sign: int) -> Fraction:
    if sign >= 0 or value == 0:
        return value
    return Fraction(-value.numerator, value.denominator, _normalize=False)


@lru_cache(maxsize=None)
def _cached_pair_gcd(left: int, right: int) -> int:
    if left <= 0 or right <= 0:
        raise ValueError("cached gcd expects positive integers")
    if left < right:
        left, right = right, left
    if right == 1:
        return 1
    if left == right:
        return left
    if max(left.bit_length(), right.bit_length()) >= _PAIR_GCD_FALLBACK_SKIP_BIT_LENGTH_CUTOFF:
        return 1
    if max(left.bit_length(), right.bit_length()) >= _PAIR_GCD_DIVISIBILITY_BIT_LENGTH_CUTOFF:
        return _exact_gcd(left, right)
    if left % right == 0:
        return right
    return _exact_gcd(left, right)


@lru_cache(maxsize=None)
def _cached_exact_quotient(value: int, divisor: int) -> int:
    if value <= 0 or divisor <= 0:
        raise ValueError("cached quotient expects positive integers")
    if divisor == 1:
        return value
    if divisor == value:
        return 1
    return _exact_quotient(value, divisor)


@lru_cache(maxsize=None)
def _cached_exact_product(left: int, right: int) -> int:
    if left <= 0 or right <= 0:
        raise ValueError("cached product expects positive integers")
    if left < right:
        left, right = right, left
    if right == 1:
        return left
    if left == right:
        return _exact_product(left, left)
    if right & (right - 1) == 0:
        return left << (right.bit_length() - 1)
    return _exact_product(left, right)


def _signed_exact_product(value: int, scale: int) -> int:
    return _exact_integer_product(value, scale)


def _exact_integer_product(left: int, right: int) -> int:
    if left == 0 or right == 0:
        return 0
    if left == 1:
        return right
    if right == 1:
        return left
    if left == -1:
        return -right
    if right == -1:
        return -left
    sign = 1
    if left < 0:
        sign = -sign
        left = -left
    if right < 0:
        sign = -sign
        right = -right
    product = _cached_exact_product(left, right)
    return product if sign > 0 else -product


@lru_cache(maxsize=None)
def _exact_prime_power(prime: int, exponent: int) -> int:
    if prime <= 1 or exponent < 0:
        raise ValueError("prime power expects prime > 1 and exponent >= 0")
    if exponent == 0:
        return 1
    if prime == 2:
        return 1 << exponent
    return prime**exponent


def _scaled_reciprocal_sum_term(*, numerator: int, denominator: int, scale: int) -> Fraction:
    scaled_numerator, scaled_denominator = _scaled_reciprocal_sum_components(
        numerator=numerator,
        denominator=denominator,
        scale=scale,
    )
    return Fraction(scaled_numerator, scaled_denominator, _normalize=False)


def _scaled_reciprocal_sum_components(*, numerator: int, denominator: int, scale: int) -> tuple[int, int]:
    if numerator == 0:
        return 0, 1
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    common_divisor = gcd(abs(numerator), scale)
    return (
        numerator // common_divisor,
        (scale // common_divisor) * denominator,
    )


def _constant_series(value: Fraction, truncated_degree: int) -> tuple[Fraction, ...]:
    return (value,) + tuple(Fraction(0) for _ in range(truncated_degree))


def _linear_series(constant: int, slope: int, truncated_degree: int) -> tuple[Fraction, ...]:
    coefficients = [Fraction(constant)]
    if truncated_degree >= 1:
        coefficients.append(Fraction(slope))
    while len(coefficients) <= truncated_degree:
        coefficients.append(Fraction(0))
    return tuple(coefficients)


def _inverse_linear_power_series(*, delta: int, exponent: int, truncated_degree: int) -> tuple[Fraction, ...]:
    coefficients = []
    for degree in range(truncated_degree + 1):
        coefficients.append(Fraction(((-1) ** degree) * comb(exponent + degree - 1, degree), delta ** (exponent + degree)))
    return tuple(coefficients)


def _multiply_truncated_series(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
    truncated_degree: int,
) -> tuple[Fraction, ...]:
    coefficients = [Fraction(0) for _ in range(truncated_degree + 1)]
    for left_degree, left_value in enumerate(left):
        if left_degree > truncated_degree or left_value == 0:
            continue
        for right_degree, right_value in enumerate(right):
            degree = left_degree + right_degree
            if degree > truncated_degree:
                break
            if right_value != 0:
                coefficients[degree] += left_value * right_value
    return tuple(coefficients)


def _build_f7_series_rational_expression(b: tuple[int, ...], mu: object) -> object:
    sympy = _load_sympy()
    b0, *tail = b
    expression = b0 + 2 * mu + 2
    expression *= _factorial_ratio_linear(mu=mu, top=b0 + 1, bottom=0)
    for value in tail:
        expression *= _factorial_ratio_linear(mu=mu, top=value, bottom=b0 - value + 1)
    return sympy.together(sympy.expand(_sympy_fraction(f7_arithmetic_renormalization(b)) * expression))


def _factorial_ratio_linear(*, mu: object, top: int, bottom: int) -> object:
    sympy = _load_sympy()
    if top == bottom:
        return sympy.Integer(1)
    if top > bottom:
        expression = sympy.Integer(1)
        for shift in range(bottom + 1, top + 1):
            expression *= mu + shift
        return expression
    expression = sympy.Integer(1)
    for shift in range(top + 1, bottom + 1):
        expression *= mu + shift
    return sympy.Rational(1, 1) / expression


def _parse_apart_term(term: object, mu: object) -> tuple[Fraction, int | None, int | None]:
    sympy = _load_sympy()
    numerator, denominator = sympy.fraction(term)
    denominator_poly = sympy.Poly(denominator, mu)
    leading_coefficient = denominator_poly.LC()
    monic_denominator = sympy.factor(denominator / leading_coefficient)
    coefficient = _fraction_from_sympy(sympy.Rational(numerator) / leading_coefficient)
    if monic_denominator == 1:
        return coefficient, None, None
    if isinstance(monic_denominator, sympy.Pow):
        base, power = monic_denominator.as_base_exp()
    else:
        base, power = monic_denominator, sympy.Integer(1)
    base_poly = sympy.Poly(sympy.expand(base), mu)
    if base_poly.degree() != 1 or base_poly.LC() != 1:
        raise ValueError(f"unexpected partial-fraction denominator: {monic_denominator!r}")
    shift = int(base_poly.TC())
    return coefficient, shift, int(power)


def _combine_harmonic_number_limits(
    *,
    left_limit: int,
    right_limit: int,
    weight: int,
    left_sign: int = 1,
    right_sign: int = 1,
) -> Fraction:
    if left_limit <= 0:
        if right_sign < 0:
            return _negate_fraction(_harmonic_number(right_limit, weight))
        return _harmonic_number(right_limit, weight)
    if right_limit <= 0:
        if left_sign < 0:
            return _negate_fraction(_harmonic_number(left_limit, weight))
        return _harmonic_number(left_limit, weight)

    if left_limit >= right_limit:
        dominant_limit = left_limit
        dominant_sign = left_sign
        secondary_limit = right_limit
        secondary_sign = right_sign
    else:
        dominant_limit = right_limit
        dominant_sign = right_sign
        secondary_limit = left_limit
        secondary_sign = left_sign

    dominant_numerator, dominant_denominator = _harmonic_number_raw_pair(dominant_limit, weight)
    secondary_numerator, secondary_denominator = _harmonic_number_raw_pair(secondary_limit, weight)

    if dominant_sign < 0:
        dominant_numerator = -dominant_numerator
    if secondary_sign < 0:
        secondary_numerator = -secondary_numerator

    if dominant_limit == secondary_limit:
        return _fraction_from_integer_pair(dominant_numerator + secondary_numerator, dominant_denominator)

    scale = _cached_exact_quotient(dominant_denominator, secondary_denominator)
    return _fraction_from_integer_pair(
        dominant_numerator + _signed_exact_product(secondary_numerator, scale),
        dominant_denominator,
    )


def _harmonic_number(limit: int, weight: int) -> Fraction:
    if limit <= 0:
        return Fraction(0)
    table = _ensure_harmonic_number_table(limit, weight)
    value = table.reduced_values[limit]
    if value is None:
        value = _fraction_from_integer_pair(table.numerators[limit], table.denominators[limit])
        table.reduced_values[limit] = value
    return value


def _harmonic_number_raw_pair(limit: int, weight: int) -> tuple[int, int]:
    if limit <= 0:
        return 0, 1
    table = _ensure_harmonic_number_table(limit, weight)
    return table.numerators[limit], table.denominators[limit]


def _ensure_harmonic_number_table(limit: int, weight: int) -> _HarmonicPowerTable:
    table = _HARMONIC_NUMBER_TABLES.get(weight)
    if table is None:
        table = _HarmonicPowerTable(
            numerators=[0],
            denominators=[1],
            reduced_values=[Fraction(0)],
        )
        _HARMONIC_NUMBER_TABLES[weight] = table

    while len(table.numerators) <= limit:
        index = len(table.numerators)
        denominator_multiplier = _harmonic_denominator_multiplier(index, weight)
        previous_denominator = table.denominators[-1]
        if denominator_multiplier == 1:
            denominator = previous_denominator
            numerator = table.numerators[-1]
        else:
            denominator = _cached_exact_product(previous_denominator, denominator_multiplier)
            numerator = _signed_exact_product(table.numerators[-1], denominator_multiplier)

        numerator += denominator // (index**weight)
        table.numerators.append(numerator)
        table.denominators.append(denominator)
        table.reduced_values.append(None)

    return table


@lru_cache(maxsize=None)
def _harmonic_denominator_multiplier(index: int, weight: int) -> int:
    if index <= 1:
        return 1
    factorization = _prime_factorization(index)
    if len(factorization) != 1:
        return 1
    return factorization[0][0] ** weight


def _fraction_from_integer_pair(numerator: int, denominator: int) -> Fraction:
    if numerator == 0:
        return Fraction(0)
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    if max(abs(numerator).bit_length(), denominator.bit_length()) >= _FINAL_SUM_NORMALIZATION_GCD_BIT_LENGTH_CUTOFF:
        return Fraction(numerator, denominator, _normalize=False)
    reduction_divisor = gcd(abs(numerator), denominator)
    if reduction_divisor != 1:
        numerator //= reduction_divisor
        denominator //= reduction_divisor
    return Fraction(numerator, denominator, _normalize=False)


def _cancel_prime_power(value: int, prime: int, exponent: int) -> tuple[int, int]:
    if value == 1 or exponent <= 0:
        return value, exponent
    if prime == 2:
        low_bit = value & -value
        removed = min(low_bit.bit_length() - 1, exponent)
        if removed == 0:
            return value, exponent
        return value >> removed, exponent - removed
    if exponent <= 2:
        if value.bit_length() >= _PRIME_STRIP_SMALL_QUOTIENT_BIT_LENGTH_CUTOFF:
            return value, exponent
        while exponent > 0 and value % prime == 0:
            value = _exact_quotient(value, prime)
            exponent -= 1
        return value, exponent
    if value.bit_length() >= _PRIME_STRIP_REMOVE_BIT_LENGTH_CUTOFF:
        return value, exponent
    if gmpy2 is not None:
        reduced_value, multiplicity = gmpy2.remove(gmpy2.mpz(value), prime)
        if multiplicity <= 0:
            return value, exponent
        removed = min(int(multiplicity), exponent)
        if removed == int(multiplicity):
            return int(reduced_value), exponent - removed
        return _exact_product(int(reduced_value), prime ** (int(multiplicity) - removed)), exponent - removed
    while exponent > 0 and value % prime == 0:
        value = _exact_quotient(value, prime)
        exponent -= 1
    return value, exponent


def _f7_arithmetic_renormalization_factorials(b: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    b0, b1, b2, b3, b4, b5, b6, b7 = b
    return (
        (
            b0 - b1 - b6,
            b0 - b1 - b7,
            b0 - b2 - b7,
            b0 - b3 - b5,
            b0 - b4 - b5,
            b0 - b4 - b6,
        ),
        (b2, b3),
    )


def _pole_constant_fraction(
    *,
    shift: int,
    normalization_numerator_factorials: tuple[int, ...],
    normalization_denominator_factorials: tuple[int, ...],
    max_shift: int,
    shift_intervals: tuple[tuple[int, int], ...],
    central_shift: int | None,
) -> Fraction:
    sign = -1 if (shift - 1) % 2 else 1
    numerator_scalar = 1
    denominator_scalar = 1
    numerator_factorials = list(normalization_numerator_factorials)
    denominator_factorials = list(normalization_denominator_factorials)

    numerator_factorials.append(shift - 1)
    numerator_factorials.append(max_shift - shift)

    if central_shift is None:
        linear_delta = max_shift + 1 - 2 * shift
        if linear_delta < 0:
            sign *= -1
            linear_delta = -linear_delta
        numerator_scalar *= linear_delta
    else:
        numerator_scalar *= 2
        if central_shift != shift:
            central_delta = central_shift - shift
            if central_delta < 0:
                sign *= -1
                central_delta = -central_delta
            numerator_scalar *= central_delta

    for left, right in shift_intervals:
        if shift < left:
            numerator_factorials.append(left - shift - 1)
            denominator_factorials.append(right - shift)
            continue
        if shift > right:
            if (right - left + 1) % 2:
                sign *= -1
            numerator_factorials.append(shift - right - 1)
            denominator_factorials.append(shift - left)
            continue
        if (shift - left) % 2:
            sign *= -1
        denominator_factorials.append(shift - left)
        denominator_factorials.append(right - shift)

    return _factorization_to_fraction(
        _pole_constant_factorization(
            shift=shift,
            normalization_numerator_factorials=normalization_numerator_factorials,
            normalization_denominator_factorials=normalization_denominator_factorials,
            max_shift=max_shift,
            shift_intervals=shift_intervals,
            central_shift=central_shift,
        )
    )


@lru_cache(maxsize=None)
def _pole_constant_factorization(
    *,
    shift: int,
    normalization_numerator_factorials: tuple[int, ...],
    normalization_denominator_factorials: tuple[int, ...],
    max_shift: int,
    shift_intervals: tuple[tuple[int, int], ...],
    central_shift: int | None,
) -> _FactorizedRational:
    sign = -1 if (shift - 1) % 2 else 1
    numerator_scalar = 1
    denominator_scalar = 1
    numerator_factorials = list(normalization_numerator_factorials)
    denominator_factorials = list(normalization_denominator_factorials)

    numerator_factorials.append(shift - 1)
    numerator_factorials.append(max_shift - shift)

    if central_shift is None:
        linear_delta = max_shift + 1 - 2 * shift
        if linear_delta < 0:
            sign *= -1
            linear_delta = -linear_delta
        numerator_scalar *= linear_delta
    else:
        numerator_scalar *= 2
        if central_shift != shift:
            central_delta = central_shift - shift
            if central_delta < 0:
                sign *= -1
                central_delta = -central_delta
            numerator_scalar *= central_delta

    for left, right in shift_intervals:
        if shift < left:
            numerator_factorials.append(left - shift - 1)
            denominator_factorials.append(right - shift)
            continue
        if shift > right:
            if (right - left + 1) % 2:
                sign *= -1
            numerator_factorials.append(shift - right - 1)
            denominator_factorials.append(shift - left)
            continue
        if (shift - left) % 2:
            sign *= -1
        denominator_factorials.append(shift - left)
        denominator_factorials.append(right - shift)

    factorization = _factorial_argument_ratio_factorization(
        numerator_factorials=tuple(numerator_factorials),
        denominator_factorials=tuple(denominator_factorials),
        numerator_scalar=numerator_scalar,
        denominator_scalar=denominator_scalar,
    )
    if sign < 0:
        return _FactorizedRational(sign=-factorization.sign, prime_exponents=factorization.prime_exponents)
    return factorization


def _factorial_argument_ratio_fraction(
    *,
    numerator_factorials: tuple[int, ...],
    denominator_factorials: tuple[int, ...],
    numerator_scalar: int = 1,
    denominator_scalar: int = 1,
) -> Fraction:
    return _factorization_to_fraction(
        _factorial_argument_ratio_factorization(
            numerator_factorials=numerator_factorials,
            denominator_factorials=denominator_factorials,
            numerator_scalar=numerator_scalar,
            denominator_scalar=denominator_scalar,
        )
    )


@lru_cache(maxsize=None)
def _factorial_argument_ratio_factorization(
    *,
    numerator_factorials: tuple[int, ...],
    denominator_factorials: tuple[int, ...],
    numerator_scalar: int = 1,
    denominator_scalar: int = 1,
) -> _FactorizedRational:
    max_factorial_argument = max((*numerator_factorials, *denominator_factorials), default=0)
    _ensure_factorial_prime_exponents(max_factorial_argument)

    sign = -1 if numerator_scalar < 0 else 1
    prime_exponents: dict[int, int] = {}
    _accumulate_prime_exponents(prime_exponents, abs(numerator_scalar), exponent=1)
    _accumulate_prime_exponents(prime_exponents, denominator_scalar, exponent=-1)
    for argument, exponent in _coalesced_factorial_argument_counts(
        numerator_factorials=numerator_factorials,
        denominator_factorials=denominator_factorials,
    ):
        if exponent:
            _accumulate_factorial_prime_exponents(prime_exponents, argument, exponent=exponent)
    return _FactorizedRational(
        sign=sign,
        prime_exponents=tuple((prime, exponent) for prime, exponent in sorted(prime_exponents.items()) if exponent),
    )


@lru_cache(maxsize=None)
def _coalesced_factorial_argument_counts(
    *,
    numerator_factorials: tuple[int, ...],
    denominator_factorials: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    factorial_argument_counts: dict[int, int] = {}
    for argument in numerator_factorials:
        if argument > 1:
            factorial_argument_counts[argument] = factorial_argument_counts.get(argument, 0) + 1
    for argument in denominator_factorials:
        if argument > 1:
            factorial_argument_counts[argument] = factorial_argument_counts.get(argument, 0) - 1
    return tuple((argument, exponent) for argument, exponent in factorial_argument_counts.items() if exponent)


def _factorization_to_fraction(value: _FactorizedRational) -> Fraction:
    numerator = value.sign
    denominator = 1
    for prime, exponent in value.prime_exponents:
        if exponent > 0:
            numerator = _signed_exact_product(numerator, prime**exponent)
        elif exponent < 0:
            denominator = _cached_exact_product(denominator, prime ** (-exponent))
    return Fraction(numerator, denominator)


def _multiply_factorized_rational_by_fraction(left: _FactorizedRational, right: Fraction) -> Fraction:
    numerator, denominator = _multiply_factorized_rational_components(
        left,
        numerator=right.numerator,
        denominator=right.denominator,
    )
    return _fraction_from_integer_pair(numerator, denominator)


def _multiply_factorized_rational_by_fraction_components(
    left: _FactorizedRational,
    right: Fraction,
) -> tuple[int, int]:
    return _multiply_factorized_rational_components(
        left,
        numerator=right.numerator,
        denominator=right.denominator,
    )


def _multiply_factorized_rational_components(
    left: _FactorizedRational,
    *,
    numerator: int,
    denominator: int,
) -> tuple[int, int]:
    if numerator == 0:
        return 0, 1
    numerator = numerator if left.sign > 0 else -numerator
    numerator_abs = abs(numerator)
    numerator_factor_exponents: dict[int, int] = {}
    denominator_factor_exponents: dict[int, int] = {}

    for prime, exponent in left.prime_exponents:
        if exponent > 0:
            denominator, exponent = _cancel_prime_power(denominator, prime, exponent)
            if exponent:
                numerator_factor_exponents[prime] = numerator_factor_exponents.get(prime, 0) + exponent
        elif exponent < 0:
            numerator_abs, remaining = _cancel_prime_power(numerator_abs, prime, -exponent)
            if remaining:
                denominator_factor_exponents[prime] = denominator_factor_exponents.get(prime, 0) + remaining

    numerator_sign = -1 if numerator < 0 else 1
    if gmpy2 is not None and numerator_factor_exponents:
        numerator_multiplier = gmpy2.mpz(1)
        for prime, exponent in numerator_factor_exponents.items():
            numerator_multiplier *= _exact_prime_power(prime, exponent)
        numerator_abs = int(gmpy2.mpz(numerator_abs) * numerator_multiplier)
    else:
        numerator_multiplier = 1
        for prime, exponent in numerator_factor_exponents.items():
            numerator_multiplier = _exact_integer_product(numerator_multiplier, _exact_prime_power(prime, exponent))
        numerator_abs = _exact_integer_product(numerator_abs, numerator_multiplier)

    if gmpy2 is not None and denominator_factor_exponents:
        denominator_multiplier = gmpy2.mpz(1)
        for prime, exponent in denominator_factor_exponents.items():
            denominator_multiplier *= _exact_prime_power(prime, exponent)
        denominator = int(gmpy2.mpz(denominator) * denominator_multiplier)
    else:
        denominator_multiplier = 1
        for prime, exponent in denominator_factor_exponents.items():
            denominator_multiplier = _cached_exact_product(denominator_multiplier, _exact_prime_power(prime, exponent))
        denominator = _cached_exact_product(denominator, denominator_multiplier)

    numerator = numerator_abs if numerator_sign > 0 else -numerator_abs
    return numerator, denominator


def _accumulate_prime_exponents(prime_exponents: dict[int, int], value: int, *, exponent: int) -> None:
    if value <= 1 or exponent == 0:
        return
    if value < len(_PRIME_FACTORIZATION_TABLE):
        factorization = _PRIME_FACTORIZATION_TABLE[value]
    else:
        factorization = _prime_factorization(value)
    get_exponent = prime_exponents.get
    if exponent == 1:
        for factor, multiplicity in factorization:
            updated_exponent = get_exponent(factor, 0) + multiplicity
            prime_exponents[factor] = updated_exponent
    elif exponent == -1:
        pop_exponent = prime_exponents.pop
        for factor, multiplicity in factorization:
            updated_exponent = get_exponent(factor, 0) - multiplicity
            if updated_exponent:
                prime_exponents[factor] = updated_exponent
            else:
                pop_exponent(factor, None)
    else:
        scaled_exponent = exponent
        pop_exponent = prime_exponents.pop
        for factor, multiplicity in factorization:
            updated_exponent = get_exponent(factor, 0) + scaled_exponent * multiplicity
            if updated_exponent:
                prime_exponents[factor] = updated_exponent
            else:
                pop_exponent(factor, None)


def _accumulate_factorial_prime_exponents(prime_exponents: dict[int, int], factorial_argument: int, *, exponent: int) -> None:
    if factorial_argument <= 1 or exponent == 0:
        return
    factorial_prime_exponents = _factorial_prime_exponents(factorial_argument)
    get_exponent = prime_exponents.get
    if exponent == 1:
        for factor, multiplicity in factorial_prime_exponents:
            updated_exponent = get_exponent(factor, 0) + multiplicity
            prime_exponents[factor] = updated_exponent
        return
    if exponent == -1:
        pop_exponent = prime_exponents.pop
        for factor, multiplicity in factorial_prime_exponents:
            updated_exponent = get_exponent(factor, 0) - multiplicity
            if updated_exponent:
                prime_exponents[factor] = updated_exponent
            else:
                pop_exponent(factor, None)
        return
    scaled_exponent = exponent
    pop_exponent = prime_exponents.pop
    for factor, multiplicity in factorial_prime_exponents:
        updated_exponent = get_exponent(factor, 0) + scaled_exponent * multiplicity
        if updated_exponent:
            prime_exponents[factor] = updated_exponent
        else:
            pop_exponent(factor, None)


def _ensure_smallest_prime_factors(limit: int) -> None:
    if limit < len(_SMALLEST_PRIME_FACTOR_TABLE):
        return
    old_limit = len(_SMALLEST_PRIME_FACTOR_TABLE) - 1
    _SMALLEST_PRIME_FACTOR_TABLE.extend(range(old_limit + 1, limit + 1))
    for factor in range(2, int(limit**0.5) + 1):
        start = factor * factor
        if start > limit:
            break
        if _SMALLEST_PRIME_FACTOR_TABLE[factor] != factor:
            continue
        first_multiple = max(start, ((old_limit + factor) // factor) * factor)
        for multiple in range(first_multiple, limit + 1, factor):
            if _SMALLEST_PRIME_FACTOR_TABLE[multiple] == multiple:
                _SMALLEST_PRIME_FACTOR_TABLE[multiple] = factor


def _ensure_prime_factorizations(limit: int) -> None:
    if limit < len(_PRIME_FACTORIZATION_TABLE):
        return
    _ensure_smallest_prime_factors(limit)
    while len(_PRIME_FACTORIZATION_TABLE) <= limit:
        value = len(_PRIME_FACTORIZATION_TABLE)
        factor = _SMALLEST_PRIME_FACTOR_TABLE[value]
        remaining = value // factor
        remaining_factors = _PRIME_FACTORIZATION_TABLE[remaining]
        if remaining_factors and remaining_factors[0][0] == factor:
            head_factor, head_multiplicity = remaining_factors[0]
            factorization = ((head_factor, head_multiplicity + 1),) + remaining_factors[1:]
        else:
            factorization = ((factor, 1),) + remaining_factors
        _PRIME_FACTORIZATION_TABLE.append(factorization)


def _ensure_factorial_prime_exponents(limit: int) -> None:
    if limit < len(_FACTORIAL_PRIME_EXPONENT_TABLE):
        return
    _ensure_prime_factorizations(limit)
    while len(_FACTORIAL_PRIME_EXPONENT_TABLE) <= limit:
        value = len(_FACTORIAL_PRIME_EXPONENT_TABLE)
        previous = _FACTORIAL_PRIME_EXPONENT_TABLE[-1]
        delta = _PRIME_FACTORIZATION_TABLE[value]
        _FACTORIAL_PRIME_EXPONENT_TABLE.append(_merge_prime_exponent_tuples(previous, delta))


def _merge_prime_exponent_tuples(
    left: tuple[tuple[int, int], ...],
    right: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    merged: list[tuple[int, int]] = []
    left_index = 0
    right_index = 0
    left_count = len(left)
    right_count = len(right)
    while left_index < left_count and right_index < right_count:
        left_prime, left_exponent = left[left_index]
        right_prime, right_exponent = right[right_index]
        if left_prime == right_prime:
            merged.append((left_prime, left_exponent + right_exponent))
            left_index += 1
            right_index += 1
            continue
        if left_prime < right_prime:
            merged.append((left_prime, left_exponent))
            left_index += 1
            continue
        merged.append((right_prime, right_exponent))
        right_index += 1
    if left_index < left_count:
        merged.extend(left[left_index:])
    if right_index < right_count:
        merged.extend(right[right_index:])
    return tuple(merged)


def _factorial_prime_exponents(limit: int) -> tuple[tuple[int, int], ...]:
    if limit <= 1:
        return ()
    _ensure_factorial_prime_exponents(limit)
    return _FACTORIAL_PRIME_EXPONENT_TABLE[limit]


def _prime_factorization(value: int) -> tuple[tuple[int, int], ...]:
    if value <= 1:
        return ()
    _ensure_prime_factorizations(value)
    return _PRIME_FACTORIZATION_TABLE[value]


def _exact_factorial(limit: int) -> int:
    if limit < 0:
        raise ValueError("factorial input must be nonnegative")
    while len(_FACTORIAL_TABLE) <= limit:
        index = len(_FACTORIAL_TABLE)
        _FACTORIAL_TABLE.append(_FACTORIAL_TABLE[-1] * index)
    return _FACTORIAL_TABLE[limit]


def _fraction_from_sympy(value: object) -> Fraction:
    sympy = _load_sympy()
    rational = sympy.Rational(value)
    return Fraction(int(rational.p), int(rational.q))


def _sympy_fraction(value: Fraction) -> object:
    sympy = _load_sympy()
    return sympy.Rational(value.numerator, value.denominator)


def _load_sympy() -> object:
    import sympy

    return sympy
