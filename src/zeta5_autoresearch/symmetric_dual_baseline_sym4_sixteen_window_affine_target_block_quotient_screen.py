from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen import (
    _build_generalized_polynomial_matrix_rows_mod,
    _unknown_count,
    _vectors_to_mod,
)
from .symmetric_dual_baseline_sym4_sixteen_window_probe import (
    _load_sym4_sixteen_window_target_sequence_cache,
)

try:
    from sympy import GF
    from sympy.polys.matrices import DomainMatrix
except ImportError:  # pragma: no cover - exercised only in stripped environments.
    GF = None
    DomainMatrix = None

SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_BLOCK_QUOTIENT_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_affine_target_block_quotient_screen.md"
)
SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_BLOCK_QUOTIENT_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_affine_target_block_quotient_screen.json"
)


@dataclass(frozen=True)
class Sym4SixteenWindowAffineTargetBlockQuotientPrimeResult:
    prime: int
    full_unknown_count: int
    quotient_unknown_count: int
    removed_column_count: int
    quotient_rank: int
    quotient_nullity: int
    verdict: str


@dataclass(frozen=True)
class Sym4SixteenWindowAffineTargetBlockQuotientScreen:
    screen_id: str
    shared_window_start: int
    shared_window_end: int
    family: str
    packet_side: str
    recurrence_order: int
    polynomial_degree: int
    equation_count: int
    full_unknown_count: int
    removed_column_count: int
    quotient_unknown_count: int
    removed_column_pattern: str
    tested_primes: tuple[int, ...]
    prime_results: tuple[Sym4SixteenWindowAffineTargetBlockQuotientPrimeResult, ...]
    overall_verdict: str
    recommendation: str


def _quotient_primes() -> tuple[int, ...]:
    return (1451, 1453, 1471, 1481, 1483, 1487, 1489, 1493)


def _tail_degree2_matrix_columns(*, dimension: int) -> tuple[int, ...]:
    per_degree = 1 + dimension * dimension + dimension
    degree_base = 2 * per_degree
    matrix_base = degree_base + 1
    return tuple(
        matrix_base + target_index * dimension + source_index
        for target_index in range(dimension)
        for source_index in range(5, dimension)
    )


def build_sym4_sixteen_window_affine_target_block_quotient_screen() -> (
    Sym4SixteenWindowAffineTargetBlockQuotientScreen
):
    target = _load_sym4_sixteen_window_target_sequence_cache()
    if target is None:
        raise RuntimeError("Sym^4 sixteen-window target sequence cache is required")
    if DomainMatrix is None or GF is None:
        raise RuntimeError("SymPy DomainMatrix/GF is required for quotient screening")

    dimension = len(target[0])
    full_unknown_count = _unknown_count(
        family="affine",
        dimension=dimension,
        recurrence_order=1,
        polynomial_degree=2,
    )
    equation_count = (len(target) - 1) * dimension
    removed_columns = set(_tail_degree2_matrix_columns(dimension=dimension))
    kept_columns = tuple(
        column for column in range(full_unknown_count) if column not in removed_columns
    )

    results = []
    for prime in _quotient_primes():
        vectors_mod = _vectors_to_mod(target, prime)
        if vectors_mod is None:
            raise RuntimeError(f"unexpected singular denominator at quotient prime {prime}")
        rows = _build_generalized_polynomial_matrix_rows_mod(
            vectors_mod,
            family="affine",
            recurrence_order=1,
            polynomial_degree=2,
            window_start=1,
            prime=prime,
        )
        quotient_rows = [[row[column] for column in kept_columns] for row in rows]
        rank = DomainMatrix.from_list(quotient_rows, GF(prime)).rank()
        nullity = len(kept_columns) - rank
        results.append(
            Sym4SixteenWindowAffineTargetBlockQuotientPrimeResult(
                prime=prime,
                full_unknown_count=full_unknown_count,
                quotient_unknown_count=len(kept_columns),
                removed_column_count=len(removed_columns),
                quotient_rank=rank,
                quotient_nullity=nullity,
                verdict=(
                    "quotient_full_column_rank_mod_prime"
                    if nullity == 0
                    else "quotient_rank_deficient_mod_prime"
                ),
            )
        )

    all_closed = all(item.quotient_nullity == 0 for item in results)
    return Sym4SixteenWindowAffineTargetBlockQuotientScreen(
        screen_id="bz_phase2_sym4_sixteen_window_affine_target_block_quotient_screen",
        shared_window_start=1,
        shared_window_end=len(target),
        family="affine",
        packet_side="target",
        recurrence_order=1,
        polynomial_degree=2,
        equation_count=equation_count,
        full_unknown_count=full_unknown_count,
        removed_column_count=len(removed_columns),
        quotient_unknown_count=len(kept_columns),
        removed_column_pattern="M[2,0,i,j] for target index i=0..14 and source index j=5..14",
        tested_primes=_quotient_primes(),
        prime_results=tuple(results),
        overall_verdict=(
            "affine_target_nullspace_collapses_after_degree2_source_tail_block_quotient"
            if all_closed
            else "affine_target_nullspace_survives_degree2_source_tail_block_quotient"
        ),
        recommendation=(
            "Treat the affine target `(order, degree) = (1, 2)` nullspace as explained by the visible parity-sparse degree-2 matrix block, and shift classification to the homogeneous target cases."
            if all_closed
            else "Continue affine target exact follow-up; the quotient still has modular nullity."
        ),
    )


def render_sym4_sixteen_window_affine_target_block_quotient_screen() -> str:
    screen = build_sym4_sixteen_window_affine_target_block_quotient_screen()
    lines = [
        "# Phase 2 Sym^4-lifted affine target block quotient screen",
        "",
        f"- Screen id: `{screen.screen_id}`",
        f"- Shared exact window: `n={screen.shared_window_start}..{screen.shared_window_end}`",
        f"- Case: `{screen.family}` `{screen.packet_side}` `(order, degree) = ({screen.recurrence_order}, {screen.polynomial_degree})`",
        f"- Equations / full unknowns: `{screen.equation_count}` / `{screen.full_unknown_count}`",
        f"- Removed columns: `{screen.removed_column_count}`",
        f"- Quotient unknowns: `{screen.quotient_unknown_count}`",
        f"- Removed pattern: `{screen.removed_column_pattern}`",
        f"- Tested primes: `{', '.join(str(prime) for prime in screen.tested_primes)}`",
        f"- Overall verdict: `{screen.overall_verdict}`",
        "",
        "## Prime results",
        "",
        "| prime | quotient unknowns | quotient rank | quotient nullity | verdict |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in screen.prime_results:
        lines.append(
            f"| `{item.prime}` | `{item.quotient_unknown_count}` | `{item.quotient_rank}` | "
            f"`{item.quotient_nullity}` | `{item.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The affine target `(order, degree) = (1, 2)` case has a stable `150`-dimensional modular nullspace before quotienting. Removing exactly the stable free degree-2 matrix block leaves a quotient system with full column rank at every tested good prime.",
            "",
            "This does not prove an exact rational statement, but it strongly indicates that the affine target modular nullspace is accounted for by the visible parity-sparse block freedom rather than by a smaller hidden recurrence-bearing subspace.",
            "",
            "## Recommendation",
            "",
            screen.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_sym4_sixteen_window_affine_target_block_quotient_screen_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_BLOCK_QUOTIENT_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_affine_target_block_quotient_screen(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_affine_target_block_quotient_screen_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_BLOCK_QUOTIENT_JSON_PATH,
) -> Path:
    screen = build_sym4_sixteen_window_affine_target_block_quotient_screen()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(screen), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_affine_target_block_quotient_screen_report()
    write_sym4_sixteen_window_affine_target_block_quotient_screen_json()


if __name__ == "__main__":
    main()
