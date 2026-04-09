from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .models import fraction_to_canonical_string
from .zudilin_2002_bridge_probe import build_zudilin_2002_bridge_probe

ZUDILIN_2002_NORMALIZATION_MAP_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_normalization_map_probe.md"
)
ZUDILIN_2002_NORMALIZATION_MAP_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_normalization_map_probe.json"
)


@dataclass(frozen=True)
class NormalizationRatioSample:
    n: int
    baseline_zeta5: str
    bridge_zeta5: str
    baseline_over_bridge: str


@dataclass(frozen=True)
class Zudilin2002NormalizationMapProbe:
    probe_id: str
    shared_window_start: int
    shared_window_end: int
    tested_map: str
    ratio_signature: tuple[str, ...]
    scalar_candidate: str | None
    mismatch_indices: tuple[int, ...]
    verdict: str
    note: str
    next_step: str
    samples: tuple[NormalizationRatioSample, ...]


def build_zudilin_2002_normalization_map_probe(*, max_n: int = 7) -> Zudilin2002NormalizationMapProbe:
    if max_n < 1:
        raise ValueError("max_n must be positive")

    bridge = build_zudilin_2002_bridge_probe(max_n=max_n)
    shared_window_end = min(max_n, len(bridge.samples) - 1)
    if shared_window_end < 1:
        raise ValueError("normalization map probe requires at least one positive index")

    baseline_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(shared_window_end))
    bridge_zeta5 = tuple(sample.p_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])
    ratios = tuple(baseline / bridge for baseline, bridge in zip(baseline_zeta5, bridge_zeta5))
    first_ratio = ratios[0]
    mismatch_indices = tuple(index for index, ratio in enumerate(ratios, start=1) if ratio != first_ratio)
    scalar_candidate = None if mismatch_indices else fraction_to_canonical_string(first_ratio)

    samples = tuple(
        NormalizationRatioSample(
            n=n,
            baseline_zeta5=fraction_to_canonical_string(baseline),
            bridge_zeta5=fraction_to_canonical_string(bridge),
            baseline_over_bridge=fraction_to_canonical_string(ratio),
        )
        for n, (baseline, bridge, ratio) in enumerate(zip(baseline_zeta5, bridge_zeta5, ratios), start=1)
    )

    if scalar_candidate is None:
        verdict = "simple_scalar_map_fails"
        note = (
            "The exact ratios `baseline_zeta5(n) / bridge_zeta5(n)` on the shared window do not collapse to a single "
            "rational scalar. This rules out only the simplest one-parameter normalization map between the two "
            "channels on n=1..7."
        )
        next_step = (
            "If we continue, the next bounded experiment should test a slightly richer normalization family, such as "
            "an affine or low-degree rational-in-n rescaling, while keeping the same conservative non-equivalence policy."
        )
    else:
        verdict = "simple_scalar_map_survives"
        note = (
            "The exact ratios `baseline_zeta5(n) / bridge_zeta5(n)` collapse to a single rational scalar on the shared "
            "window, so the simplest one-parameter normalization map survives this bounded check."
        )
        next_step = (
            "Promote the surviving scalar to an explicit normalization hypothesis and test it against the companion "
            "channel before making any stronger interpretation."
        )

    return Zudilin2002NormalizationMapProbe(
        probe_id="bz_phase2_zudilin_2002_normalization_map_probe",
        shared_window_start=1,
        shared_window_end=shared_window_end,
        tested_map="baseline_zeta5(n) = c * bridge_zeta5(n) for all n on the shared window",
        ratio_signature=tuple(fraction_to_canonical_string(ratio) for ratio in ratios),
        scalar_candidate=scalar_candidate,
        mismatch_indices=mismatch_indices,
        verdict=verdict,
        note=note,
        next_step=next_step,
        samples=samples,
    )


def render_zudilin_2002_normalization_map_probe(*, max_n: int = 7) -> str:
    probe = build_zudilin_2002_normalization_map_probe(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 normalization map probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Tested map: `{probe.tested_map}`",
        f"- Verdict: `{probe.verdict}`",
        f"- Scalar candidate: `{probe.scalar_candidate}`" if probe.scalar_candidate is not None else "- Scalar candidate: none",
        f"- Mismatch indices: `{','.join(str(index) for index in probe.mismatch_indices)}`"
        if probe.mismatch_indices
        else "- Mismatch indices: none",
        "",
        "| n | baseline zeta(5) | bridge zeta(5) | baseline / bridge |",
        "| --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.baseline_zeta5}` | `{sample.bridge_zeta5}` | `{sample.baseline_over_bridge}` |"
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


def write_zudilin_2002_normalization_map_probe_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_NORMALIZATION_MAP_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_normalization_map_probe(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_normalization_map_probe_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_NORMALIZATION_MAP_JSON_PATH,
) -> Path:
    probe = build_zudilin_2002_normalization_map_probe(max_n=max_n)
    payload = asdict(probe)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_normalization_map_probe_report()
    write_zudilin_2002_normalization_map_probe_json()


if __name__ == "__main__":
    main()
