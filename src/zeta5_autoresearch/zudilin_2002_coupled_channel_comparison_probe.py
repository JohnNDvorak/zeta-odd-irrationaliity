from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .zudilin_2002_bridge_probe import build_zudilin_2002_bridge_probe
from .zudilin_2002_coupled_channel_comparison_target import (
    ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_TARGET_REPORT_PATH,
    build_zudilin_2002_coupled_channel_comparison_target,
)

ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_coupled_channel_comparison_probe.md"
)
ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_coupled_channel_comparison_probe.json"
)


@dataclass(frozen=True)
class CoupledComparisonSample:
    n: int
    baseline_pair: tuple[str, str]
    bridge_pair: tuple[str, str]


@dataclass(frozen=True)
class Zudilin2002CoupledChannelComparisonProbe:
    probe_id: str
    target_id: str
    shared_window_start: int
    shared_window_end: int
    baseline_pair_hash: str
    bridge_pair_hash: str
    verdict: str
    asymmetry: str
    recommendation: str
    samples: tuple[CoupledComparisonSample, ...]


def build_zudilin_2002_coupled_channel_comparison_probe(
    *, max_n: int = 7
) -> Zudilin2002CoupledChannelComparisonProbe:
    target = build_zudilin_2002_coupled_channel_comparison_target(max_n=max_n)
    bridge = build_zudilin_2002_bridge_probe(max_n=max_n)
    shared_window_end = target.shared_window_end

    baseline_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(shared_window_end))
    baseline_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(shared_window_end, component="zeta3")
    bridge_zeta5 = tuple(sample.p_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])
    bridge_zeta3 = tuple(sample.ptilde_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])

    baseline_pairs = tuple(zip(baseline_zeta5, baseline_zeta3))
    bridge_pairs = tuple(zip(bridge_zeta5, bridge_zeta3))

    baseline_pair_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "zudilin_2002_coupled_baseline_pair",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "pairs": [
                {
                    "n": index,
                    "zeta5": fraction_to_canonical_string(pair[0]),
                    "zeta3": fraction_to_canonical_string(pair[1]),
                }
                for index, pair in enumerate(baseline_pairs, start=1)
            ],
        }
    )
    bridge_pair_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "zudilin_2002_coupled_bridge_pair",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "pairs": [
                {
                    "n": index,
                    "zeta5": fraction_to_canonical_string(pair[0]),
                    "zeta3": fraction_to_canonical_string(pair[1]),
                }
                for index, pair in enumerate(bridge_pairs, start=1)
            ],
        }
    )

    samples = tuple(
        CoupledComparisonSample(
            n=n,
            baseline_pair=(
                fraction_to_canonical_string(base_pair[0]),
                fraction_to_canonical_string(base_pair[1]),
            ),
            bridge_pair=(
                fraction_to_canonical_string(bridge_pair_item[0]),
                fraction_to_canonical_string(bridge_pair_item[1]),
            ),
        )
        for n, (base_pair, bridge_pair_item) in enumerate(zip(baseline_pairs, bridge_pairs), start=1)
        if n <= 3
    )

    return Zudilin2002CoupledChannelComparisonProbe(
        probe_id="bz_phase2_zudilin_2002_coupled_channel_comparison_probe",
        target_id=target.target_id,
        shared_window_start=1,
        shared_window_end=shared_window_end,
        baseline_pair_hash=baseline_pair_hash,
        bridge_pair_hash=bridge_pair_hash,
        verdict="coupled_comparison_ready_but_not_equivalent",
        asymmetry=(
            "The baseline side is a finite-window exact ordered pair, while the bridge side is a recurrence-explicit ordered pair. "
            "This probe compares paired object shape and reproducibility, not recurrence-level equivalence."
        ),
        recommendation=(
            "If we continue, the next bounded step should test one coupled transformation hypothesis on the ordered pair, "
            "not another one-channel normalization family."
        ),
        samples=samples,
    )


def render_zudilin_2002_coupled_channel_comparison_probe(*, max_n: int = 7) -> str:
    probe = build_zudilin_2002_coupled_channel_comparison_probe(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 coupled-channel comparison probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Coupled comparison target: `{ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_TARGET_REPORT_PATH}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Baseline pair hash: `{probe.baseline_pair_hash}`",
        f"- Bridge pair hash: `{probe.bridge_pair_hash}`",
        f"- Verdict: `{probe.verdict}`",
        "",
        "## Asymmetry",
        "",
        probe.asymmetry,
        "",
        "## Sample paired data",
        "",
        "| n | baseline (ζ(5), ζ(3)) | bridge (ζ(5), ζ(3)) |",
        "| --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `({sample.baseline_pair[0]}, {sample.baseline_pair[1]})` | `({sample.bridge_pair[0]}, {sample.bridge_pair[1]})` |"
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            probe.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_zudilin_2002_coupled_channel_comparison_probe_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_coupled_channel_comparison_probe(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_coupled_channel_comparison_probe_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_PROBE_JSON_PATH,
) -> Path:
    probe = build_zudilin_2002_coupled_channel_comparison_probe(max_n=max_n)
    payload = asdict(probe)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_coupled_channel_comparison_probe_report()
    write_zudilin_2002_coupled_channel_comparison_probe_json()


if __name__ == "__main__":
    main()
