from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .config import DEFAULT_CONVERGENCE_SCAN_LIMIT, DEFAULT_CONVERGENCE_START_N
from .models import AffineFamily
from .translate import s_to_a


def _is_integral(value: Fraction) -> bool:
    return value.denominator == 1


@dataclass(frozen=True)
class ParityCheckResult:
    valid: bool
    failures: tuple[str, ...]


@dataclass(frozen=True)
class LinearFormCheck:
    name: str
    slope: Fraction
    intercept: Fraction
    first_value: Fraction
    all_n_nonnegative: bool


@dataclass(frozen=True)
class ConvergenceCheckResult:
    valid: bool
    asymptotically_valid: bool
    failures: tuple[str, ...]
    linear_forms: tuple[LinearFormCheck, ...]
    scan_values: dict[int, tuple[Fraction, ...]]


def check_all_n_parity(affine_family: AffineFamily) -> ParityCheckResult:
    failures: list[str] = []
    for values, label in ((affine_family.u, "u"), (affine_family.v, "v")):
        for i in range(8):
            for j in range(8):
                if not _is_integral(values[i] - values[j]):
                    failures.append(f"{label}[{i}] - {label}[{j}] is not integral")
    return ParityCheckResult(valid=not failures, failures=tuple(failures))


def _linear_forms(a: tuple[Fraction, ...]) -> tuple[tuple[str, Fraction], ...]:
    a1, a2, a3, a4, a5, a6, a7, a8 = a
    return (
        ("a1", a1),
        ("a2", a2),
        ("a3", a3),
        ("a4", a4),
        ("a5", a5),
        ("a6", a6),
        ("a7", a7),
        ("a1+a5-a3", a1 + a5 - a3),
        ("a3+a6-a8", a3 + a6 - a8),
        ("a4+a5+a7+a8-a2-a3-a6", a4 + a5 + a7 + a8 - a2 - a3 - a6),
        ("a7+a8-a6", a7 + a8 - a6),
        ("a4+a8-a2", a4 + a8 - a2),
        ("a2+a3+a6-a4-a8", a2 + a3 + a6 - a4 - a8),
        ("a1+a8-a3", a1 + a8 - a3),
        ("a1+a2-a4", a1 + a2 - a4),
        ("a4+a5-a2", a4 + a5 - a2),
        ("a4+a7+2*a8-a2-a3-a6", a4 + a7 + 2 * a8 - a2 - a3 - a6),
    )


def check_convergence(
    affine_family: AffineFamily,
    *,
    start_n: int = DEFAULT_CONVERGENCE_START_N,
    scan_limit: int = DEFAULT_CONVERGENCE_SCAN_LIMIT,
) -> ConvergenceCheckResult:
    if start_n < 0:
        raise ValueError("start_n must be nonnegative")
    if scan_limit < start_n:
        raise ValueError("scan_limit must be >= start_n")

    slope_forms = _linear_forms(s_to_a(affine_family.u))
    intercept_forms = _linear_forms(s_to_a(affine_family.v))

    failures: list[str] = []
    checks: list[LinearFormCheck] = []
    asymptotically_valid = True

    for (name, slope), (_, intercept) in zip(slope_forms, intercept_forms, strict=True):
        first_value = slope * start_n + intercept
        all_n_nonnegative = slope >= 0 and first_value >= 0
        if slope < 0:
            asymptotically_valid = False
            failures.append(f"{name} has negative slope {slope}")
        elif first_value < 0:
            failures.append(f"{name} is negative at n={start_n}: {first_value}")
        checks.append(
            LinearFormCheck(
                name=name,
                slope=slope,
                intercept=intercept,
                first_value=first_value,
                all_n_nonnegative=all_n_nonnegative,
            )
        )

    scan_values: dict[int, tuple[Fraction, ...]] = {}
    for n in range(start_n, scan_limit + 1):
        forms_at_n = tuple(slope * n + intercept for (_, slope), (_, intercept) in zip(slope_forms, intercept_forms, strict=True))
        scan_values[n] = forms_at_n
        negatives = [str(value) for value in forms_at_n if value < 0]
        if negatives:
            failures.append(f"negative convergence form encountered at n={n}: {', '.join(negatives)}")

    return ConvergenceCheckResult(
        valid=not failures,
        asymptotically_valid=asymptotically_valid,
        failures=tuple(dict.fromkeys(failures)),
        linear_forms=tuple(checks),
        scan_values=scan_values,
    )
