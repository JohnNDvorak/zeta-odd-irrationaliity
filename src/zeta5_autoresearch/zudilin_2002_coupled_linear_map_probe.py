from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .models import fraction_to_canonical_string
from .zudilin_2002_bridge_probe import build_zudilin_2002_bridge_probe
from .zudilin_2002_coupled_channel_comparison_probe import (
    ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_PROBE_REPORT_PATH,
)

ZUDILIN_2002_COUPLED_LINEAR_MAP_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_coupled_linear_map_probe.md"
)
ZUDILIN_2002_COUPLED_LINEAR_MAP_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_coupled_linear_map_probe.json"
)


@dataclass(frozen=True)
class CoupledLinearMapSample:
    n: int
    observed_baseline_pair: tuple[str, str]
    predicted_baseline_pair: tuple[str, str]
    matches_linear_map: bool


@dataclass(frozen=True)
class Zudilin2002CoupledLinearMapProbe:
    probe_id: str
    shared_window_start: int
    shared_window_end: int
    tested_map: str
    matrix_entries: tuple[tuple[str, str], tuple[str, str]]
    mismatch_indices: tuple[int, ...]
    verdict: str
    note: str
    next_step: str
    samples: tuple[CoupledLinearMapSample, ...]


def build_zudilin_2002_coupled_linear_map_probe(*, max_n: int = 7) -> Zudilin2002CoupledLinearMapProbe:
    if max_n < 2:
        raise ValueError("max_n must be at least 2")

    bridge = build_zudilin_2002_bridge_probe(max_n=max_n)
    shared_window_end = min(max_n, len(bridge.samples) - 1)
    if shared_window_end < 2:
        raise ValueError("coupled linear map probe requires at least two positive indices")

    baseline_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(shared_window_end))
    baseline_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(shared_window_end, component="zeta3")
    bridge_zeta5 = tuple(sample.p_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])
    bridge_zeta3 = tuple(sample.ptilde_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])

    bridge_v1 = (bridge_zeta5[0], bridge_zeta3[0])
    bridge_v2 = (bridge_zeta5[1], bridge_zeta3[1])
    baseline_v1 = (baseline_zeta5[0], baseline_zeta3[0])
    baseline_v2 = (baseline_zeta5[1], baseline_zeta3[1])

    matrix = _solve_linear_map(bridge_v1, bridge_v2, baseline_v1, baseline_v2)

    predicted_pairs = tuple(
        _apply_matrix(matrix, (bridge5, bridge3))
        for bridge5, bridge3 in zip(bridge_zeta5, bridge_zeta3)
    )
    observed_pairs = tuple(zip(baseline_zeta5, baseline_zeta3))
    mismatch_indices = tuple(
        index
        for index, (observed, predicted) in enumerate(zip(observed_pairs, predicted_pairs), start=1)
        if observed != predicted
    )

    samples = tuple(
        CoupledLinearMapSample(
            n=n,
            observed_baseline_pair=(
                fraction_to_canonical_string(observed[0]),
                fraction_to_canonical_string(observed[1]),
            ),
            predicted_baseline_pair=(
                fraction_to_canonical_string(predicted[0]),
                fraction_to_canonical_string(predicted[1]),
            ),
            matches_linear_map=observed == predicted,
        )
        for n, (observed, predicted) in enumerate(zip(observed_pairs, predicted_pairs), start=1)
        if n <= 3
    )

    if mismatch_indices:
        verdict = "constant_coupled_linear_map_fails"
        note = (
            "A single constant `2x2` rational linear transformation, fitted from `n=1,2`, does not carry the Zudilin "
            "ordered pair to the baseline ordered pair on the full shared window. This closes the simplest coupled linear ansatz."
        )
        next_step = (
            "If we continue on coupled maps, the next bounded family should allow `n`-dependence or another structured "
            "two-channel transformation, not just a constant matrix."
        )
    else:
        verdict = "constant_coupled_linear_map_survives"
        note = (
            "A single constant `2x2` rational linear transformation carries the Zudilin ordered pair to the baseline "
            "ordered pair on the shared window."
        )
        next_step = (
            "Promote the surviving matrix to an explicit coupled-map hypothesis and test whether it remains compatible "
            "with the rest of the bridge-comparison constraints."
        )

    return Zudilin2002CoupledLinearMapProbe(
        probe_id="bz_phase2_zudilin_2002_coupled_linear_map_probe",
        shared_window_start=1,
        shared_window_end=shared_window_end,
        tested_map="baseline_pair(n) = M * bridge_pair(n) for a constant rational 2x2 matrix M on the shared window",
        matrix_entries=(
            (
                fraction_to_canonical_string(matrix[0][0]),
                fraction_to_canonical_string(matrix[0][1]),
            ),
            (
                fraction_to_canonical_string(matrix[1][0]),
                fraction_to_canonical_string(matrix[1][1]),
            ),
        ),
        mismatch_indices=mismatch_indices,
        verdict=verdict,
        note=note,
        next_step=next_step,
        samples=samples,
    )


def render_zudilin_2002_coupled_linear_map_probe(*, max_n: int = 7) -> str:
    probe = build_zudilin_2002_coupled_linear_map_probe(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 coupled linear map probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Coupled comparison probe: `{ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_PROBE_REPORT_PATH}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Tested map: `{probe.tested_map}`",
        f"- Verdict: `{probe.verdict}`",
        f"- Matrix row 1: `({probe.matrix_entries[0][0]}, {probe.matrix_entries[0][1]})`",
        f"- Matrix row 2: `({probe.matrix_entries[1][0]}, {probe.matrix_entries[1][1]})`",
        (
            f"- Mismatch indices: `{','.join(str(index) for index in probe.mismatch_indices)}`"
            if probe.mismatch_indices
            else "- Mismatch indices: none"
        ),
        "",
        "| n | observed baseline pair | predicted pair | matches |",
        "| --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `({sample.observed_baseline_pair[0]}, {sample.observed_baseline_pair[1]})` | "
            f"`({sample.predicted_baseline_pair[0]}, {sample.predicted_baseline_pair[1]})` | `{sample.matches_linear_map}` |"
        )
    lines.extend(
        [
            "",
            "## Note",
            "",
            probe.note,
            "",
            "## Next step",
            "",
            probe.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_zudilin_2002_coupled_linear_map_probe_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_LINEAR_MAP_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_coupled_linear_map_probe(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_coupled_linear_map_probe_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_LINEAR_MAP_JSON_PATH,
) -> Path:
    probe = build_zudilin_2002_coupled_linear_map_probe(max_n=max_n)
    payload = asdict(probe)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def _solve_linear_map(
    bridge_v1: tuple[Fraction, Fraction],
    bridge_v2: tuple[Fraction, Fraction],
    baseline_v1: tuple[Fraction, Fraction],
    baseline_v2: tuple[Fraction, Fraction],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    determinant = bridge_v1[0] * bridge_v2[1] - bridge_v2[0] * bridge_v1[1]
    if determinant == 0:
        raise ValueError("bridge seed vectors are linearly dependent on n=1,2; cannot fit a constant 2x2 map")

    inverse = (
        (bridge_v2[1] / determinant, -bridge_v2[0] / determinant),
        (-bridge_v1[1] / determinant, bridge_v1[0] / determinant),
    )
    return (
        (
            baseline_v1[0] * inverse[0][0] + baseline_v2[0] * inverse[1][0],
            baseline_v1[0] * inverse[0][1] + baseline_v2[0] * inverse[1][1],
        ),
        (
            baseline_v1[1] * inverse[0][0] + baseline_v2[1] * inverse[1][0],
            baseline_v1[1] * inverse[0][1] + baseline_v2[1] * inverse[1][1],
        ),
    )


def _apply_matrix(
    matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
    vector: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def main() -> None:
    write_zudilin_2002_coupled_linear_map_probe_report()
    write_zudilin_2002_coupled_linear_map_probe_json()


if __name__ == "__main__":
    main()
