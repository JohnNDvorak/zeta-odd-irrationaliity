from __future__ import annotations

import hashlib
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

SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_NULLSPACE_FINGERPRINT_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint.md"
)
SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_NULLSPACE_FINGERPRINT_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint.json"
)

SOURCE_BOUNDARY = (
    "A success on this object would still be a bounded exact transfer statement on the shared "
    "Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common "
    "recurrence, or reopen the frozen `n=435` lane."
)


@dataclass(frozen=True)
class Sym4SixteenWindowAffineTargetNullspacePrimeFingerprint:
    prime: int
    rank: int | None
    nullity: int | None
    pivot_count: int | None
    free_columns: tuple[int, ...]
    free_column_labels: tuple[str, ...]
    pivot_columns_hash: str | None
    domainmatrix_nullspace_hash: str | None
    domainmatrix_nullspace_row_count: int | None
    domainmatrix_nullspace_row_rank: int | None
    domainmatrix_nullspace_support_size_min: int | None
    domainmatrix_nullspace_support_size_max: int | None
    verified_nullspace_rows_against_matrix: bool
    verdict: str


@dataclass(frozen=True)
class Sym4SixteenWindowAffineTargetNullspaceFingerprint:
    fingerprint_id: str
    shared_window_start: int
    shared_window_end: int
    family: str
    packet_side: str
    recurrence_order: int
    polynomial_degree: int
    matrix_size: int
    equation_count: int
    unknown_count: int
    tested_primes: tuple[int, ...]
    minimum_good_prime_nullity: int | None
    minimum_nullity_primes: tuple[int, ...]
    stable_free_columns: tuple[int, ...]
    stable_free_column_labels: tuple[str, ...]
    prime_results: tuple[Sym4SixteenWindowAffineTargetNullspacePrimeFingerprint, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _fingerprint_primes() -> tuple[int, ...]:
    return (1451, 1453, 1471, 1481, 1483, 1487, 1489, 1493)


def _hash_payload(payload: object) -> str:
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _free_columns_summary(columns: tuple[int, ...]) -> str:
    if not columns:
        return ""
    runs = []
    run_start = columns[0]
    previous = columns[0]
    for column in columns[1:]:
        if column == previous + 1:
            previous = column
            continue
        runs.append(f"{run_start}" if run_start == previous else f"{run_start}..{previous}")
        run_start = column
        previous = column
    runs.append(f"{run_start}" if run_start == previous else f"{run_start}..{previous}")
    return ", ".join(runs)


def _column_label(column: int, *, dimension: int, recurrence_order: int) -> str:
    per_degree = 1 + recurrence_order * dimension * dimension + dimension
    degree, offset = divmod(column, per_degree)
    if offset == 0:
        return f"a[{degree}]"
    matrix_block_size = recurrence_order * dimension * dimension
    if offset <= matrix_block_size:
        matrix_offset = offset - 1
        block, block_offset = divmod(matrix_offset, dimension * dimension)
        target_index, source_index = divmod(block_offset, dimension)
        return f"M[{degree},{block},{target_index},{source_index}]"
    translation_index = offset - 1 - matrix_block_size
    return f"t[{degree},{translation_index}]"


def _verify_basis(
    rows: list[list[int]],
    basis: tuple[tuple[int, ...], ...],
    *,
    prime: int,
) -> bool:
    for vector in basis:
        support = tuple(index for index, value in enumerate(vector) if value)
        for row in rows:
            total = sum(row[index] * vector[index] for index in support) % prime
            if total:
                return False
    return True


def _rank_mod_rows(
    rows: tuple[tuple[int, ...], ...],
    *,
    variable_count: int,
    prime: int,
) -> int:
    matrix = [list(row) for row in rows]
    pivot_row = 0
    for column in range(variable_count):
        pivot_index = None
        for row_index in range(pivot_row, len(matrix)):
            if matrix[row_index][column] % prime != 0:
                pivot_index = row_index
                break
        if pivot_index is None:
            continue
        if pivot_index != pivot_row:
            matrix[pivot_row], matrix[pivot_index] = matrix[pivot_index], matrix[pivot_row]
        pivot = matrix[pivot_row][column] % prime
        inverse = pow(pivot, -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for row_index in range(pivot_row + 1, len(matrix)):
            factor = matrix[row_index][column] % prime
            if factor:
                matrix[row_index] = [
                    (value - factor * basis) % prime
                    for value, basis in zip(matrix[row_index], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def _prime_fingerprint(
    vectors,
    *,
    prime: int,
    dimension: int,
    variable_count: int,
) -> Sym4SixteenWindowAffineTargetNullspacePrimeFingerprint:
    vectors_mod = _vectors_to_mod(vectors, prime)
    if vectors_mod is None:
        return Sym4SixteenWindowAffineTargetNullspacePrimeFingerprint(
            prime=prime,
            rank=None,
            nullity=None,
            pivot_count=None,
            free_columns=(),
            free_column_labels=(),
            pivot_columns_hash=None,
            domainmatrix_nullspace_hash=None,
            domainmatrix_nullspace_row_count=None,
            domainmatrix_nullspace_row_rank=None,
            domainmatrix_nullspace_support_size_min=None,
            domainmatrix_nullspace_support_size_max=None,
            verified_nullspace_rows_against_matrix=False,
            verdict="skipped_denominator_singular_mod_prime",
        )
    rows = _build_generalized_polynomial_matrix_rows_mod(
        vectors_mod,
        family="affine",
        recurrence_order=1,
        polynomial_degree=2,
        window_start=1,
        prime=prime,
    )
    if DomainMatrix is None or GF is None:
        raise RuntimeError("SymPy DomainMatrix/GF is required for nullspace fingerprinting")
    matrix = DomainMatrix.from_list(rows, GF(prime))
    rank = matrix.rank()
    _, pivots = matrix.rref()
    pivots = tuple(int(column) for column in pivots)
    free_columns = tuple(column for column in range(variable_count) if column not in set(pivots))
    nullspace = matrix.nullspace()
    nullspace_rows = tuple(
        tuple(int(entry) % prime for entry in row)
        for row in nullspace.to_list()
    )
    verified = _verify_basis(rows, nullspace_rows, prime=prime)
    nullspace_row_count = len(nullspace_rows)
    nullspace_row_rank = _rank_mod_rows(
        nullspace_rows,
        variable_count=variable_count,
        prime=prime,
    )
    support_sizes = tuple(sum(1 for value in row if value) for row in nullspace_rows)
    nullity = variable_count - rank
    nullspace_rank_matches = nullspace_row_rank == nullity
    return Sym4SixteenWindowAffineTargetNullspacePrimeFingerprint(
        prime=prime,
        rank=rank,
        nullity=nullity,
        pivot_count=len(pivots),
        free_columns=free_columns,
        free_column_labels=tuple(
            _column_label(column, dimension=dimension, recurrence_order=1)
            for column in free_columns
        ),
        pivot_columns_hash=_hash_payload(pivots),
        domainmatrix_nullspace_hash=_hash_payload(nullspace_rows),
        domainmatrix_nullspace_row_count=nullspace_row_count,
        domainmatrix_nullspace_row_rank=nullspace_row_rank,
        domainmatrix_nullspace_support_size_min=min(support_sizes) if support_sizes else None,
        domainmatrix_nullspace_support_size_max=max(support_sizes) if support_sizes else None,
        verified_nullspace_rows_against_matrix=verified,
        verdict=(
            "verified_nullspace_basis_mod_prime"
            if verified and nullspace_rank_matches
            else "verified_redundant_nullspace_rows_mod_prime"
            if verified
            else "basis_verification_failed"
        ),
    )


def build_sym4_sixteen_window_affine_target_nullspace_fingerprint() -> (
    Sym4SixteenWindowAffineTargetNullspaceFingerprint
):
    target = _load_sym4_sixteen_window_target_sequence_cache()
    if target is None:
        raise RuntimeError("Sym^4 sixteen-window target sequence cache is required")
    dimension = len(target[0])
    variable_count = _unknown_count(
        family="affine",
        dimension=dimension,
        recurrence_order=1,
        polynomial_degree=2,
    )
    equation_count = (len(target) - 1) * dimension
    prime_results = tuple(
        _prime_fingerprint(
            target,
            prime=prime,
            dimension=dimension,
            variable_count=variable_count,
        )
        for prime in _fingerprint_primes()
    )
    good_results = tuple(item for item in prime_results if item.nullity is not None)
    minimum_nullity = min((item.nullity for item in good_results), default=None)
    minimum_results = tuple(
        item for item in good_results if item.nullity == minimum_nullity
    )
    minimum_primes = tuple(item.prime for item in minimum_results)
    stable_free_columns = ()
    stable_free_labels = ()
    if minimum_results:
        first_free_columns = minimum_results[0].free_columns
        if all(item.free_columns == first_free_columns for item in minimum_results):
            stable_free_columns = first_free_columns
            stable_free_labels = minimum_results[0].free_column_labels
    all_verified = all(
        item.verified_nullspace_rows_against_matrix
        and item.domainmatrix_nullspace_row_rank == item.nullity
        for item in minimum_results
    )
    stable_profile = bool(stable_free_columns) and all_verified
    return Sym4SixteenWindowAffineTargetNullspaceFingerprint(
        fingerprint_id="bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint",
        shared_window_start=1,
        shared_window_end=len(target),
        family="affine",
        packet_side="target",
        recurrence_order=1,
        polynomial_degree=2,
        matrix_size=dimension,
        equation_count=equation_count,
        unknown_count=variable_count,
        tested_primes=_fingerprint_primes(),
        minimum_good_prime_nullity=minimum_nullity,
        minimum_nullity_primes=minimum_primes,
        stable_free_columns=stable_free_columns,
        stable_free_column_labels=stable_free_labels,
        prime_results=prime_results,
        overall_verdict=(
            "affine_target_modular_nullspace_has_stable_free_column_profile"
            if stable_profile
            else "affine_target_modular_nullspace_requires_additional_fingerprinting"
        ),
        source_boundary=SOURCE_BOUNDARY,
        recommendation=(
            "Build a verified canonical modular basis from the stable pivot/free-column profile, then attempt CRT/rational reconstruction and exact residual verification for affine target `(order, degree) = (1, 2)`."
            if stable_profile
            else "Do not attempt exact reconstruction until the modular free-column profile and nullspace-row verification are both stable."
        ),
    )


def render_sym4_sixteen_window_affine_target_nullspace_fingerprint() -> str:
    fingerprint = build_sym4_sixteen_window_affine_target_nullspace_fingerprint()
    lines = [
        "# Phase 2 Sym^4-lifted affine target nullspace fingerprint",
        "",
        f"- Fingerprint id: `{fingerprint.fingerprint_id}`",
        f"- Shared exact window: `n={fingerprint.shared_window_start}..{fingerprint.shared_window_end}`",
        f"- Case: `{fingerprint.family}` `{fingerprint.packet_side}` `(order, degree) = ({fingerprint.recurrence_order}, {fingerprint.polynomial_degree})`",
        f"- Matrix size: `{fingerprint.matrix_size}`",
        f"- Equations / unknowns: `{fingerprint.equation_count}` / `{fingerprint.unknown_count}`",
        f"- Tested primes: `{', '.join(str(prime) for prime in fingerprint.tested_primes)}`",
        f"- Minimum good-prime nullity: `{fingerprint.minimum_good_prime_nullity}`",
        f"- Minimum-nullity primes: `{', '.join(str(prime) for prime in fingerprint.minimum_nullity_primes)}`",
        f"- Overall verdict: `{fingerprint.overall_verdict}`",
        "",
        "## Prime fingerprints",
        "",
        "| prime | rank | nullity | pivot count | free columns | nullspace rows | nullspace row rank | support range | verified | verdict |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in fingerprint.prime_results:
        support_range = (
            ""
            if item.domainmatrix_nullspace_support_size_min is None
            else f"{item.domainmatrix_nullspace_support_size_min}..{item.domainmatrix_nullspace_support_size_max}"
        )
        free_columns = _free_columns_summary(item.free_columns)
        lines.append(
            f"| `{item.prime}` | `{item.rank}` | `{item.nullity}` | `{item.pivot_count}` | "
            f"`{free_columns}` | "
            f"`{item.domainmatrix_nullspace_row_count}` | "
            f"`{item.domainmatrix_nullspace_row_rank}` | "
            f"`{support_range}` | "
            f"`{item.verified_nullspace_rows_against_matrix}` | `{item.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Stable free columns",
            "",
        ]
    )
    if fingerprint.stable_free_columns:
        lines.append(
            f"- Count: `{len(fingerprint.stable_free_columns)}`"
        )
        lines.append(
            f"- Column runs: `{_free_columns_summary(fingerprint.stable_free_columns)}`"
        )
        lines.append(
            "- Label pattern: `M[2,0,i,j]` for target index `i=0..14` and source index `j=5..14`."
        )
        lines.append("- The full column and label list is preserved in the JSON cache artifact.")
    else:
        lines.append("- No stable free-column profile was found on the minimum-nullity primes.")
    lines.extend(
        [
            "",
            "## Hashes",
            "",
            "| prime | pivot columns hash | DomainMatrix nullspace hash |",
            "| --- | --- | --- |",
        ]
    )
    for item in fingerprint.prime_results:
        lines.append(
            f"| `{item.prime}` | `{item.pivot_columns_hash}` | `{item.domainmatrix_nullspace_hash}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is a modular nullspace fingerprint for the smallest persistent generalized target-side case. It does not certify an exact rational recurrence. Its purpose is to identify whether the modular nullspaces have a stable shape suitable for a separately verified canonical modular basis, CRT/rational reconstruction, and exact residual verification.",
            "",
            "## Source boundary",
            "",
            fingerprint.source_boundary,
            "",
            "## Recommendation",
            "",
            fingerprint.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_sym4_sixteen_window_affine_target_nullspace_fingerprint_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_NULLSPACE_FINGERPRINT_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_affine_target_nullspace_fingerprint(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_affine_target_nullspace_fingerprint_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_AFFINE_TARGET_NULLSPACE_FINGERPRINT_JSON_PATH,
) -> Path:
    fingerprint = build_sym4_sixteen_window_affine_target_nullspace_fingerprint()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(fingerprint), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_affine_target_nullspace_fingerprint_report()
    write_sym4_sixteen_window_affine_target_nullspace_fingerprint_json()


if __name__ == "__main__":
    main()
