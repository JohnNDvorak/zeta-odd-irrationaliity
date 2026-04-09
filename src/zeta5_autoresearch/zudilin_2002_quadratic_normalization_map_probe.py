from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .models import fraction_to_canonical_string
from .zudilin_2002_bridge_probe import build_zudilin_2002_bridge_probe

ZUDILIN_2002_QUADRATIC_NORMALIZATION_MAP_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_quadratic_normalization_map_probe.md"
)
ZUDILIN_2002_QUADRATIC_NORMALIZATION_MAP_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_quadratic_normalization_map_probe.json"
)


@dataclass(frozen=True)
class QuadraticNormalizationSample:
    n: int
    observed_ratio: str
    predicted_ratio: str
    matches_quadratic_candidate: bool


@dataclass(frozen=True)
class Zudilin2002QuadraticNormalizationMapProbe:
    probe_id: str
    shared_window_start: int
    shared_window_end: int
    tested_map: str
    quadratic_a: str
    quadratic_b: str
    quadratic_c: str
    mismatch_indices: tuple[int, ...]
    verdict: str
    note: str
    next_step: str
    samples: tuple[QuadraticNormalizationSample, ...]


def build_zudilin_2002_quadratic_normalization_map_probe(
    *, max_n: int = 7
) -> Zudilin2002QuadraticNormalizationMapProbe:
    if max_n < 3:
        raise ValueError("max_n must be at least 3")

    bridge = build_zudilin_2002_bridge_probe(max_n=max_n)
    shared_window_end = min(max_n, len(bridge.samples) - 1)
    if shared_window_end < 3:
        raise ValueError("quadratic normalization map probe requires at least three positive indices")

    baseline_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(shared_window_end))
    bridge_zeta5 = tuple(sample.p_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])
    ratios = tuple(baseline / bridge for baseline, bridge in zip(baseline_zeta5, bridge_zeta5))

    q_a, q_b, q_c = _fit_quadratic(ratios[0], ratios[1], ratios[2])
    predicted = tuple(q_a * n * n + q_b * n + q_c for n in range(1, shared_window_end + 1))
    mismatch_indices = tuple(index for index, (lhs, rhs) in enumerate(zip(ratios, predicted), start=1) if lhs != rhs)

    samples = tuple(
        QuadraticNormalizationSample(
            n=n,
            observed_ratio=fraction_to_canonical_string(observed),
            predicted_ratio=fraction_to_canonical_string(predicted_ratio),
            matches_quadratic_candidate=observed == predicted_ratio,
        )
        for n, (observed, predicted_ratio) in enumerate(zip(ratios, predicted), start=1)
    )

    if mismatch_indices:
        verdict = "quadratic_scalar_map_fails"
        note = (
            "The exact ratios `baseline_zeta5(n) / bridge_zeta5(n)` do not lie on a single quadratic polynomial "
            "`a n^2 + b n + c` over the shared window. This rules out a third bounded normalization family."
        )
        next_step = (
            "The normalization line is now expensive relative to its signal. The next clean move is a decision artifact "
            "that banks the scalar/affine/quadratic failures and recommends either stopping here or switching to a "
            "different bridge comparison ansatz."
        )
    else:
        verdict = "quadratic_scalar_map_survives"
        note = (
            "The exact ratios fit a single quadratic polynomial `a n^2 + b n + c` on the shared window, so the "
            "quadratic normalization family survives this bounded check."
        )
        next_step = (
            "Promote the quadratic candidate to an explicit normalization hypothesis and test whether the companion "
            "zeta(3) channel respects the same quadratic structure."
        )

    return Zudilin2002QuadraticNormalizationMapProbe(
        probe_id="bz_phase2_zudilin_2002_quadratic_normalization_map_probe",
        shared_window_start=1,
        shared_window_end=shared_window_end,
        tested_map="baseline_zeta5(n) = (a*n^2 + b*n + c) * bridge_zeta5(n) for all n on the shared window",
        quadratic_a=fraction_to_canonical_string(q_a),
        quadratic_b=fraction_to_canonical_string(q_b),
        quadratic_c=fraction_to_canonical_string(q_c),
        mismatch_indices=mismatch_indices,
        verdict=verdict,
        note=note,
        next_step=next_step,
        samples=samples,
    )


def render_zudilin_2002_quadratic_normalization_map_probe(*, max_n: int = 7) -> str:
    probe = build_zudilin_2002_quadratic_normalization_map_probe(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 quadratic normalization map probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Tested map: `{probe.tested_map}`",
        f"- Verdict: `{probe.verdict}`",
        f"- Quadratic a: `{probe.quadratic_a}`",
        f"- Quadratic b: `{probe.quadratic_b}`",
        f"- Quadratic c: `{probe.quadratic_c}`",
        (
            f"- Mismatch indices: `{','.join(str(index) for index in probe.mismatch_indices)}`"
            if probe.mismatch_indices
            else "- Mismatch indices: none"
        ),
        "",
        "| n | observed ratio | predicted quadratic ratio | matches |",
        "| --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.observed_ratio}` | `{sample.predicted_ratio}` | `{sample.matches_quadratic_candidate}` |"
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


def write_zudilin_2002_quadratic_normalization_map_probe_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_QUADRATIC_NORMALIZATION_MAP_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_quadratic_normalization_map_probe(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_quadratic_normalization_map_probe_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_QUADRATIC_NORMALIZATION_MAP_JSON_PATH,
) -> Path:
    probe = build_zudilin_2002_quadratic_normalization_map_probe(max_n=max_n)
    payload = asdict(probe)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def _fit_quadratic(y1: Fraction, y2: Fraction, y3: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    a = (y3 - 2 * y2 + y1) / 2
    b = y2 - y1 - 3 * a
    c = y1 - a - b
    return a, b, c


def main() -> None:
    write_zudilin_2002_quadratic_normalization_map_probe_report()
    write_zudilin_2002_quadratic_normalization_map_probe_json()


if __name__ == "__main__":
    main()
