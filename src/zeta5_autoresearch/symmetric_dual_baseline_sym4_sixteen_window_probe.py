from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import json
from time import perf_counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from multiprocessing import get_all_start_methods, get_context
import os
from pathlib import Path
import sys

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_packet_schur_functor import build_sym4_lifted_packet_vectors
from .dual_packet_window_plucker import (
    _advance_codimension_one_common_den_state,
    _common_denominator_rows,
    _integerize_vectors,
    _invert_basis_columns,
    _matvec_rows_common_den,
    _recover_codimension_one_coordinates,
    build_normalized_window_maximal_minor_vectors,
)
from .hashes import compute_sequence_hash
from .models import _fraction_from_decimal_string, _int_to_decimal_string, fraction_to_canonical_string
from .symmetric_dual_baseline_sym4_sixteen_window_object_spec import (
    SYM4_SIXTEEN_WINDOW_OBJECT_SPEC_REPORT_PATH,
    build_sym4_sixteen_window_object_spec,
)
from .symmetric_dual_full_packet import build_symmetric_dual_full_packet

SYM4_SIXTEEN_WINDOW_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_probe.md"
)
SYM4_SIXTEEN_WINDOW_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_probe.json"
)
SYM4_SIXTEEN_WINDOW_TARGET_PARTIAL_CACHE_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_target_partial_cache.json"
)
SYM4_SIXTEEN_WINDOW_TARGET_SEQUENCE_CACHE_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_target_sequence_cache.json"
)


Sym4SixteenWindowVector = tuple[Fraction, ...]


@dataclass(frozen=True)
class Sym4SixteenWindowSample:
    n: int
    source_values: tuple[str, ...]
    target_values: tuple[str, ...]


@dataclass(frozen=True)
class Sym4SixteenWindowProbe:
    probe_id: str
    source_spec_id: str
    shared_window_start: int
    shared_window_end: int
    coordinate_count: int
    source_invariant_hash: str
    target_invariant_hash: str
    paired_object_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    source_boundary: str
    recommendation: str
    samples: tuple[Sym4SixteenWindowSample, ...]


@dataclass(frozen=True)
class Sym4SixteenWindowTargetPartialCache:
    cache_id: str
    status: str
    window_size: int
    shared_window_start: int
    shared_window_end: int
    state_window_index: int
    coordinate_count: int
    next_window_index: int
    completed_window_count: int
    total_window_count: int
    inverse_denominator: str
    coordinate_numerators: tuple[str, ...]
    inverse_row_numerators: tuple[tuple[str, ...], ...]
    profiles: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class Sym4SixteenWindowTargetCacheProgress:
    cache_id: str
    status: str
    completed_window_count: int
    total_window_count: int
    next_window_index: int
    coordinate_count: int


def _int_from_decimal_string(text: str) -> int:
    current_limit = sys.get_int_max_str_digits()
    if current_limit == 0:
        return int(text)
    sys.set_int_max_str_digits(0)
    try:
        return int(text)
    finally:
        sys.set_int_max_str_digits(current_limit)


def _serialize_integer_tuple(values: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(_int_to_decimal_string(int(value)) for value in values)


def _deserialize_integer_tuple(values: tuple[str, ...] | list[str]) -> tuple[int, ...]:
    return tuple(_int_from_decimal_string(value) for value in values)


def _serialize_fraction_tuple(values: tuple[Fraction, ...]) -> tuple[str, ...]:
    return tuple(fraction_to_canonical_string(value) for value in values)


def _deserialize_fraction_tuple(values: tuple[str, ...] | list[str]) -> tuple[Fraction, ...]:
    return tuple(_fraction_from_decimal_string(value) for value in values)


def _build_sym4_source_packet_vectors() -> tuple[tuple[Fraction, Fraction, Fraction], ...]:
    packet = build_symmetric_dual_full_packet(max_n=80)
    return tuple(
        (packet.constant_terms[i], packet.zeta3_terms[i], packet.zeta5_terms[i])
        for i in range(80)
    )


def _build_sym4_target_packet_vectors() -> tuple[tuple[Fraction, Fraction, Fraction], ...]:
    target_constant = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    target_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    target_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))
    return tuple((target_constant[i], target_zeta3[i], target_zeta5[i]) for i in range(80))


def _load_sym4_sixteen_window_target_sequence_cache(
    cache_path: str | Path = SYM4_SIXTEEN_WINDOW_TARGET_SEQUENCE_CACHE_PATH,
) -> tuple[Sym4SixteenWindowVector, ...] | None:
    path = Path(cache_path)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(
        _deserialize_fraction_tuple(tuple(entry["values"]))
        for entry in payload["terms"]
    )


def write_sym4_sixteen_window_target_sequence_cache(
    values: tuple[Sym4SixteenWindowVector, ...],
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_TARGET_SEQUENCE_CACHE_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "cache_id": "bz_phase2_sym4_sixteen_window_target_sequence_cache",
        "shared_window_start": 1,
        "shared_window_end": len(values),
        "coordinate_count": len(values[0]) if values else 0,
        "terms": [
            {"n": index, "values": list(_serialize_fraction_tuple(vector))}
            for index, vector in enumerate(values, start=1)
        ],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def _load_sym4_sixteen_window_target_partial_cache(
    cache_path: str | Path = SYM4_SIXTEEN_WINDOW_TARGET_PARTIAL_CACHE_PATH,
) -> Sym4SixteenWindowTargetPartialCache | None:
    path = Path(cache_path)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return Sym4SixteenWindowTargetPartialCache(
        cache_id=payload["cache_id"],
        status=payload["status"],
        window_size=payload["window_size"],
        shared_window_start=payload["shared_window_start"],
        shared_window_end=payload["shared_window_end"],
        state_window_index=payload.get("state_window_index", payload["next_window_index"]),
        coordinate_count=payload["coordinate_count"],
        next_window_index=payload["next_window_index"],
        completed_window_count=payload["completed_window_count"],
        total_window_count=payload["total_window_count"],
        inverse_denominator=payload["inverse_denominator"],
        coordinate_numerators=tuple(payload["coordinate_numerators"]),
        inverse_row_numerators=tuple(tuple(row) for row in payload["inverse_row_numerators"]),
        profiles=tuple(tuple(profile) for profile in payload["profiles"]),
    )


def write_sym4_sixteen_window_target_partial_cache(
    cache: Sym4SixteenWindowTargetPartialCache,
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_TARGET_PARTIAL_CACHE_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(cache), indent=2, sort_keys=True), encoding="utf-8")
    return output


def _initialize_sym4_sixteen_window_target_partial_cache() -> Sym4SixteenWindowTargetPartialCache:
    vectors = _build_sym4_target_packet_vectors()
    lifted = build_sym4_lifted_packet_vectors(vectors)
    dimension = len(lifted[0])
    window_size = 16
    basis_scales, integer_vectors = _integerize_vectors(lifted)
    basis_fraction = tuple(
        tuple(Fraction(int(value)) for value in column)
        for column in integer_vectors[:dimension]
    )
    inverse_rows = _invert_basis_columns(basis_fraction)
    inverse_row_numerators, inverse_denominator = _common_denominator_rows(inverse_rows)
    coordinates = _matvec_rows_common_den(inverse_row_numerators, integer_vectors[dimension])
    return Sym4SixteenWindowTargetPartialCache(
        cache_id="bz_phase2_sym4_sixteen_window_target_partial_cache",
        status="in_progress",
        window_size=window_size,
        shared_window_start=1,
        shared_window_end=0,
        state_window_index=0,
        coordinate_count=dimension,
        next_window_index=0,
        completed_window_count=0,
        total_window_count=len(lifted) - window_size + 1,
        inverse_denominator=_int_to_decimal_string(int(inverse_denominator)),
        coordinate_numerators=_serialize_integer_tuple(coordinates),
        inverse_row_numerators=tuple(_serialize_integer_tuple(row) for row in inverse_row_numerators),
        profiles=(),
    )


def _rebase_sym4_sixteen_window_target_state(
    integer_vectors: tuple[tuple[int, ...], ...],
    *,
    start_window_index: int,
    dimension: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...], int]:
    basis_fraction = tuple(
        tuple(Fraction(int(value)) for value in column)
        for column in integer_vectors[start_window_index : start_window_index + dimension]
    )
    inverse_rows = _invert_basis_columns(basis_fraction)
    inverse_row_numerators, inverse_denominator = _common_denominator_rows(inverse_rows)
    coordinates = _matvec_rows_common_den(
        inverse_row_numerators,
        integer_vectors[start_window_index + dimension],
    )
    return inverse_row_numerators, coordinates, inverse_denominator


def resume_sym4_sixteen_window_target_partial_cache(
    *,
    max_runtime_seconds: float = 30.0,
    max_windows_per_run: int | None = None,
    cache_path: str | Path = SYM4_SIXTEEN_WINDOW_TARGET_PARTIAL_CACHE_PATH,
    final_cache_path: str | Path = SYM4_SIXTEEN_WINDOW_TARGET_SEQUENCE_CACHE_PATH,
) -> Sym4SixteenWindowTargetCacheProgress:
    final_cache = _load_sym4_sixteen_window_target_sequence_cache(final_cache_path)
    if final_cache is not None:
        return Sym4SixteenWindowTargetCacheProgress(
            cache_id="bz_phase2_sym4_sixteen_window_target_partial_cache",
            status="complete",
            completed_window_count=len(final_cache),
            total_window_count=len(final_cache),
            next_window_index=len(final_cache),
            coordinate_count=len(final_cache[0]),
        )

    cache = _load_sym4_sixteen_window_target_partial_cache(cache_path)
    if cache is None:
        cache = _initialize_sym4_sixteen_window_target_partial_cache()
        write_sym4_sixteen_window_target_partial_cache(cache, cache_path)

    vectors = _build_sym4_target_packet_vectors()
    lifted = build_sym4_lifted_packet_vectors(vectors)
    basis_scales, integer_vectors = _integerize_vectors(lifted)
    dimension = cache.coordinate_count
    row_numerators = tuple(
        _deserialize_integer_tuple(row)
        for row in cache.inverse_row_numerators
    )
    coordinates = _deserialize_integer_tuple(cache.coordinate_numerators)
    denominator = _int_from_decimal_string(cache.inverse_denominator)
    profiles = list(cache.profiles)
    window_count = cache.total_window_count

    start = perf_counter()
    state_window_index = cache.state_window_index
    next_window_index = cache.next_window_index
    completed_this_run = 0

    while state_window_index < next_window_index:
        if next_window_index >= window_count:
            state_window_index = next_window_index
            break
        if coordinates[0] == 0:
            row_numerators, coordinates, denominator = _rebase_sym4_sixteen_window_target_state(
                integer_vectors,
                start_window_index=state_window_index + 1,
                dimension=dimension,
            )
            state_window_index += 1
            continue
        next_extra_in_old_basis = _matvec_rows_common_den(
            row_numerators,
            integer_vectors[state_window_index + dimension],
        )
        row_numerators, coordinates, denominator = _advance_codimension_one_common_den_state(
            row_numerators,
            coordinates,
            denominator,
            next_extra_in_old_basis,
        )
        state_window_index += 1

    while next_window_index < window_count:
        profile = _recover_codimension_one_coordinates(
            coordinates,
            denominator,
            basis_scales=basis_scales[next_window_index : next_window_index + dimension],
            extra_scale=basis_scales[next_window_index + dimension],
        )
        profiles.append(_serialize_fraction_tuple(profile))
        next_window_index += 1
        completed_this_run += 1

        checkpoint = Sym4SixteenWindowTargetPartialCache(
            cache_id=cache.cache_id,
            status="complete" if next_window_index == window_count else "in_progress",
            window_size=cache.window_size,
            shared_window_start=1,
            shared_window_end=next_window_index,
            state_window_index=state_window_index,
            coordinate_count=cache.coordinate_count,
            next_window_index=next_window_index,
            completed_window_count=len(profiles),
            total_window_count=window_count,
            inverse_denominator=_int_to_decimal_string(int(denominator)),
            coordinate_numerators=_serialize_integer_tuple(coordinates),
            inverse_row_numerators=tuple(_serialize_integer_tuple(row) for row in row_numerators),
            profiles=tuple(profiles),
        )
        write_sym4_sixteen_window_target_partial_cache(checkpoint, cache_path)

        if next_window_index == window_count:
            updated = checkpoint
            break
        if max_windows_per_run is not None and completed_this_run >= max_windows_per_run:
            updated = checkpoint
            break
        if perf_counter() - start >= max_runtime_seconds:
            updated = checkpoint
            break
        if coordinates[0] == 0:
            row_numerators, coordinates, denominator = _rebase_sym4_sixteen_window_target_state(
                integer_vectors,
                start_window_index=next_window_index,
                dimension=dimension,
            )
            state_window_index = next_window_index
            continue
        next_extra_in_old_basis = _matvec_rows_common_den(
            row_numerators,
            integer_vectors[next_window_index + dimension],
        )
        row_numerators, coordinates, denominator = _advance_codimension_one_common_den_state(
            row_numerators,
            coordinates,
            denominator,
            next_extra_in_old_basis,
        )
        state_window_index = next_window_index
    else:
        updated = Sym4SixteenWindowTargetPartialCache(
            cache_id=cache.cache_id,
            status="complete" if next_window_index == window_count else "in_progress",
            window_size=cache.window_size,
            shared_window_start=1,
            shared_window_end=next_window_index,
            state_window_index=state_window_index,
            coordinate_count=cache.coordinate_count,
            next_window_index=next_window_index,
            completed_window_count=len(profiles),
            total_window_count=window_count,
            inverse_denominator=_int_to_decimal_string(int(denominator)),
            coordinate_numerators=_serialize_integer_tuple(coordinates),
            inverse_row_numerators=tuple(_serialize_integer_tuple(row) for row in row_numerators),
            profiles=tuple(profiles),
        )

    write_sym4_sixteen_window_target_partial_cache(updated, cache_path)
    if updated.status == "complete":
        final_values = tuple(_deserialize_fraction_tuple(profile) for profile in updated.profiles)
        write_sym4_sixteen_window_target_sequence_cache(final_values, final_cache_path)

    return Sym4SixteenWindowTargetCacheProgress(
        cache_id=updated.cache_id,
        status=updated.status,
        completed_window_count=updated.completed_window_count,
        total_window_count=updated.total_window_count,
        next_window_index=updated.next_window_index,
        coordinate_count=updated.coordinate_count,
    )


def _build_sym4_sixteen_window_side(side: str) -> tuple[Sym4SixteenWindowVector, ...]:
    if side == "source":
        vectors = _build_sym4_source_packet_vectors()
    elif side == "target":
        cached_target = _load_sym4_sixteen_window_target_sequence_cache()
        if cached_target is not None:
            return cached_target
        vectors = _build_sym4_target_packet_vectors()
    else:
        raise ValueError(f"unknown Sym^4 side: {side}")

    lifted = build_sym4_lifted_packet_vectors(vectors)
    return build_normalized_window_maximal_minor_vectors(lifted, window_size=16)


@lru_cache(maxsize=1)
def build_sym4_sixteen_window_sequences() -> tuple[tuple[Sym4SixteenWindowVector, ...], tuple[Sym4SixteenWindowVector, ...]]:
    if os.cpu_count() and os.cpu_count() > 1:
        start_method = "fork" if "fork" in get_all_start_methods() else "spawn"
        with ProcessPoolExecutor(max_workers=2, mp_context=get_context(start_method)) as executor:
            source_future = executor.submit(_build_sym4_sixteen_window_side, "source")
            target_future = executor.submit(_build_sym4_sixteen_window_side, "target")
            source = source_future.result()
            target = target_future.result()
    else:
        source = _build_sym4_sixteen_window_side("source")
        target = _build_sym4_sixteen_window_side("target")
    return source, target


def _payload(values: tuple[Sym4SixteenWindowVector, ...]) -> list[dict[str, object]]:
    return [
        {"n": n, "values": [fraction_to_canonical_string(value) for value in vector]}
        for n, vector in enumerate(values, start=1)
    ]


@lru_cache(maxsize=1)
def build_sym4_sixteen_window_probe() -> Sym4SixteenWindowProbe:
    spec = build_sym4_sixteen_window_object_spec()
    source, target = build_sym4_sixteen_window_sequences()
    source_payload = _payload(source)
    target_payload = _payload(target)
    source_hash = compute_sequence_hash(
        provisional_signature={"kind": "sym4_sixteen_window_source", "terms": source_payload}
    )
    target_hash = compute_sequence_hash(
        provisional_signature={"kind": "sym4_sixteen_window_target", "terms": target_payload}
    )
    paired_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "sym4_sixteen_window_transfer_object",
            "source_hash": source_hash,
            "target_hash": target_hash,
            "coordinate_count": len(source[0]),
            "shared_window_start": 1,
            "shared_window_end": len(source),
        }
    )
    samples = tuple(
        Sym4SixteenWindowSample(
            n=n,
            source_values=tuple(source_payload[n - 1]["values"][:4]),  # type: ignore[index]
            target_values=tuple(target_payload[n - 1]["values"][:4]),  # type: ignore[index]
        )
        for n in range(1, 3)
    )
    return Sym4SixteenWindowProbe(
        probe_id="bz_phase2_sym4_sixteen_window_probe",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=len(source),
        coordinate_count=len(source[0]),
        source_invariant_hash=source_hash,
        target_invariant_hash=target_hash,
        paired_object_hash=paired_hash,
        verdict="sym4_sixteen_window_object_established",
        stabilized_findings=(
            "The symmetric-dual and baseline-dual Sym^4-lifted sixteen-window invariants are now repo-native exact objects.",
            "The Sym^4-lifted sixteen-window invariant has coordinate count `15` on the shared exact window `n=1..65`.",
            "Source, target, and paired nonlinear objects are independently reproducible via exact hashes.",
        ),
        unresolved_findings=(
            "No recurrence-level transfer family has yet been certified on this Sym^4-lifted sixteen-window object.",
            "No implication for baseline `P_n` extraction follows directly from this object alone.",
            "No claim is made that the quartic Schur lift dominates every other higher nonlinear invariant family.",
        ),
        source_boundary=spec.source_boundary,
        recommendation=(
            "Run the low-order homogeneous matrix ladder through order `4` and the affine ladder through order `3` on source and target separately."
        ),
        samples=samples,
    )


def render_sym4_sixteen_window_probe() -> str:
    probe = build_sym4_sixteen_window_probe()
    lines = [
        "# Phase 2 Sym^4-lifted sixteen-window probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{SYM4_SIXTEEN_WINDOW_OBJECT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Coordinate count: `{probe.coordinate_count}`",
        f"- Source invariant hash: `{probe.source_invariant_hash}`",
        f"- Target invariant hash: `{probe.target_invariant_hash}`",
        f"- Paired object hash: `{probe.paired_object_hash}`",
        f"- Verdict: `{probe.verdict}`",
        "",
        "## Stabilized findings",
        "",
    ]
    for item in probe.stabilized_findings:
        lines.append(f"- {item}")
    lines.extend(["", "## Unresolved findings", ""])
    for item in probe.unresolved_findings:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Sample normalized coordinates",
            "",
            "| n | source first four coords | target first four coords |",
            "| --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{', '.join(sample.source_values)}` | `{', '.join(sample.target_values)}` |"
        )
    lines.extend(["", "## Source boundary", "", probe.source_boundary, "", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_sym4_sixteen_window_probe_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_probe(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_probe_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_PROBE_JSON_PATH,
) -> Path:
    probe = build_sym4_sixteen_window_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_probe_report()
    write_sym4_sixteen_window_probe_json()


if __name__ == "__main__":
    main()
