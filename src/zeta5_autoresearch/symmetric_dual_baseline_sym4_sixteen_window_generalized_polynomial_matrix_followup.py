from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen import (
    _build_generalized_polynomial_matrix_rows_mod,
    _rank_mod_matrix,
    _unknown_count,
    _vectors_to_mod,
)
from .symmetric_dual_baseline_sym4_sixteen_window_probe import (
    build_sym4_sixteen_window_probe,
    build_sym4_sixteen_window_sequences,
)

SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_FOLLOWUP_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md"
)
SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_FOLLOWUP_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.json"
)


@dataclass(frozen=True)
class Sym4SixteenWindowGeneralizedPolynomialMatrixPrimeResult:
    prime: int
    rank: int | None
    nullity: int | None
    verdict: str


@dataclass(frozen=True)
class Sym4SixteenWindowGeneralizedPolynomialMatrixFollowupCase:
    family: str
    packet_side: str
    recurrence_order: int
    polynomial_degree: int
    matrix_size: int
    equation_count: int
    unknown_count: int
    prime_results: tuple[Sym4SixteenWindowGeneralizedPolynomialMatrixPrimeResult, ...]
    case_verdict: str
    witness_prime: int | None


@dataclass(frozen=True)
class Sym4SixteenWindowGeneralizedPolynomialMatrixFollowup:
    followup_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    tested_primes: tuple[int, ...]
    case_results: tuple[Sym4SixteenWindowGeneralizedPolynomialMatrixFollowupCase, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _open_target_cases() -> tuple[tuple[str, int, int], ...]:
    return (
        ("homogeneous", 1, 2),
        ("homogeneous", 1, 3),
        ("affine", 1, 2),
    )


def _followup_primes() -> tuple[int, ...]:
    return (1451, 1009, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493)


def _case_verdict(
    prime_results: tuple[Sym4SixteenWindowGeneralizedPolynomialMatrixPrimeResult, ...],
    *,
    unknown_count: int,
) -> tuple[str, int | None]:
    for item in prime_results:
        if item.rank == unknown_count:
            return "closed_by_full_rank_mod_prime", item.prime
    return "modular_nullity_persists_on_bounded_prime_set", None


def _screen_followup_case(
    *,
    family: str,
    recurrence_order: int,
    polynomial_degree: int,
    vectors,
    window_start: int,
    primes: tuple[int, ...],
) -> Sym4SixteenWindowGeneralizedPolynomialMatrixFollowupCase:
    dimension = len(vectors[0])
    variable_count = _unknown_count(
        family=family,
        dimension=dimension,
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
    )
    equation_count = (len(vectors) - recurrence_order) * dimension
    prime_results = []
    for prime in primes:
        vectors_mod = _vectors_to_mod(vectors, prime)
        if vectors_mod is None:
            prime_results.append(
                Sym4SixteenWindowGeneralizedPolynomialMatrixPrimeResult(
                    prime=prime,
                    rank=None,
                    nullity=None,
                    verdict="skipped_denominator_singular_mod_prime",
                )
            )
            continue
        rows = _build_generalized_polynomial_matrix_rows_mod(
            vectors_mod,
            family=family,
            recurrence_order=recurrence_order,
            polynomial_degree=polynomial_degree,
            window_start=window_start,
            prime=prime,
        )
        rank = _rank_mod_matrix(rows, variable_count, prime)
        nullity = variable_count - rank
        prime_results.append(
            Sym4SixteenWindowGeneralizedPolynomialMatrixPrimeResult(
                prime=prime,
                rank=rank,
                nullity=nullity,
                verdict=(
                    "full_column_rank_mod_prime"
                    if nullity == 0
                    else "rank_deficient_mod_prime"
                ),
            )
        )

    case_verdict, witness_prime = _case_verdict(tuple(prime_results), unknown_count=variable_count)
    return Sym4SixteenWindowGeneralizedPolynomialMatrixFollowupCase(
        family=family,
        packet_side="target",
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
        matrix_size=dimension,
        equation_count=equation_count,
        unknown_count=variable_count,
        prime_results=tuple(prime_results),
        case_verdict=case_verdict,
        witness_prime=witness_prime,
    )


@lru_cache(maxsize=1)
def build_sym4_sixteen_window_generalized_polynomial_matrix_followup() -> (
    Sym4SixteenWindowGeneralizedPolynomialMatrixFollowup
):
    probe = build_sym4_sixteen_window_probe()
    _, target = build_sym4_sixteen_window_sequences()
    primes = _followup_primes()
    case_results = tuple(
        _screen_followup_case(
            family=family,
            recurrence_order=recurrence_order,
            polynomial_degree=polynomial_degree,
            vectors=target,
            window_start=probe.shared_window_start,
            primes=primes,
        )
        for family, recurrence_order, polynomial_degree in _open_target_cases()
    )
    all_closed = all(item.case_verdict == "closed_by_full_rank_mod_prime" for item in case_results)
    any_persistent = any(
        item.case_verdict == "modular_nullity_persists_on_bounded_prime_set" for item in case_results
    )
    return Sym4SixteenWindowGeneralizedPolynomialMatrixFollowup(
        followup_id="bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        tested_primes=primes,
        case_results=case_results,
        overall_verdict=(
            "generalized_polynomial_target_cases_closed_by_bounded_prime_followup"
            if all_closed
            else "generalized_polynomial_target_cases_require_exact_nullspace_followup"
            if any_persistent
            else "generalized_polynomial_target_cases_inconclusive_due_to_singular_denominators"
        ),
        source_boundary=probe.source_boundary,
        recommendation=(
            "Do not escalate generalized polynomial matrix degree/order mechanically. The bounded prime follow-up closed all previously open target-side cases."
            if all_closed
            else "Classify the persistent target-side generalized polynomial matrix nullspace structure before trying another recurrence family."
            if any_persistent
            else "Choose a new bounded prime set that avoids singular denominators before making a mathematical inference."
        ),
    )


def render_sym4_sixteen_window_generalized_polynomial_matrix_followup() -> str:
    followup = build_sym4_sixteen_window_generalized_polynomial_matrix_followup()
    lines = [
        "# Phase 2 Sym^4-lifted sixteen-window generalized polynomial matrix follow-up",
        "",
        f"- Follow-up id: `{followup.followup_id}`",
        f"- Source probe id: `{followup.source_probe_id}`",
        f"- Shared exact window: `n={followup.shared_window_start}..{followup.shared_window_end}`",
        f"- Tested primes: `{', '.join(str(prime) for prime in followup.tested_primes)}`",
        f"- Overall verdict: `{followup.overall_verdict}`",
        "",
        "## Case summary",
        "",
        "| family | side | recurrence order | polynomial degree | matrix size | equation count | unknown count | case verdict | witness prime |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in followup.case_results:
        lines.append(
            f"| `{item.family}` | `{item.packet_side}` | `{item.recurrence_order}` | `{item.polynomial_degree}` | "
            f"`{item.matrix_size}` | `{item.equation_count}` | `{item.unknown_count}` | `{item.case_verdict}` | `{item.witness_prime}` |"
        )
    lines.extend(
        [
            "",
            "## Prime ranks",
            "",
            "| family | recurrence order | polynomial degree | prime | rank | nullity | verdict |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in followup.case_results:
        for prime_result in item.prime_results:
            lines.append(
                f"| `{item.family}` | `{item.recurrence_order}` | `{item.polynomial_degree}` | "
                f"`{prime_result.prime}` | `{prime_result.rank}` | `{prime_result.nullity}` | `{prime_result.verdict}` |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This bounded follow-up revisits only the three target-side generalized polynomial matrix cases left open by the first screen. A full column rank over any good prime would obstruct an exact rational recurrence in that case. Persistent modular nullity across this finite prime set is a structured-nullspace lead, not a proof of a rational recurrence.",
            "",
            "## Source boundary",
            "",
            followup.source_boundary,
            "",
            "## Recommendation",
            "",
            followup.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_sym4_sixteen_window_generalized_polynomial_matrix_followup_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_FOLLOWUP_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_generalized_polynomial_matrix_followup(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_generalized_polynomial_matrix_followup_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_FOLLOWUP_JSON_PATH,
) -> Path:
    followup = build_sym4_sixteen_window_generalized_polynomial_matrix_followup()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(followup), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_generalized_polynomial_matrix_followup_report()
    write_sym4_sixteen_window_generalized_polynomial_matrix_followup_json()


if __name__ == "__main__":
    main()
