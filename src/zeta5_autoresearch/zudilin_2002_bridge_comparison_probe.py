from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_rule_experiment import build_phase2_dual_projection_rule_experiment
from .gate2.sequence_identity import ProvisionalSequenceIdentity, compute_provisional_sequence_hash
from .zudilin_2002_bridge_probe import (
    ZUDILIN_2002_BRIDGE_REPORT_PATH,
    build_zudilin_2002_bridge_probe,
)

ZUDILIN_2002_BRIDGE_COMPARISON_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_zudilin_2002_bridge_comparison_probe.md"
ZUDILIN_2002_BRIDGE_COMPARISON_JSON_PATH = CACHE_DIR / "bz_phase2_zudilin_2002_bridge_comparison_probe.json"


@dataclass(frozen=True)
class ZudilinBridgeChannelComparison:
    channel_id: str
    baseline_object: str
    bridge_object: str
    baseline_window_hash: str
    bridge_window_hash: str
    shared_window_end: int
    verdict: str
    note: str


@dataclass(frozen=True)
class Zudilin2002BridgeComparisonProbe:
    probe_id: str
    bridge_id: str
    shared_window_start: int
    shared_window_end: int
    channel_comparisons: tuple[ZudilinBridgeChannelComparison, ...]
    overall_verdict: str
    next_step: str


def build_zudilin_2002_bridge_comparison_probe(*, max_n: int = 7) -> Zudilin2002BridgeComparisonProbe:
    if max_n < 1:
        raise ValueError("max_n must be positive")

    baseline = build_phase2_dual_projection_rule_experiment()
    bridge = build_zudilin_2002_bridge_probe(max_n=max_n)
    shared_window_end = min(max_n, len(bridge.samples) - 1)
    if shared_window_end < 1:
        raise ValueError("bridge comparison requires at least one positive index")

    leading_bridge_signature = tuple(sample.p_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])
    companion_bridge_signature = tuple(sample.ptilde_n / sample.q_n for sample in bridge.samples[1 : shared_window_end + 1])

    baseline_leading_hash = _provisional_hash(
        component_id="baseline_retained_pair_window",
        signature=tuple(_extract_sample_fraction(sample.retained_zeta5) for sample in baseline.samples[:shared_window_end]),
    )
    bridge_leading_hash = _provisional_hash(
        component_id="zudilin_leading_bridge_window",
        signature=leading_bridge_signature,
    )
    baseline_companion_hash = _provisional_hash(
        component_id="baseline_residual_zeta3_window",
        signature=tuple(_extract_sample_fraction(sample.residual_zeta3) for sample in baseline.samples[:shared_window_end]),
    )
    bridge_companion_hash = _provisional_hash(
        component_id="zudilin_companion_bridge_window",
        signature=companion_bridge_signature,
    )

    channel_comparisons = (
        ZudilinBridgeChannelComparison(
            channel_id="leading_target_channel",
            baseline_object="baseline retained zeta(5) coefficient channel on the retained pair split",
            bridge_object="Zudilin 2002 explicit p_n / q_n bridge channel for zeta(5)",
            baseline_window_hash=baseline_leading_hash,
            bridge_window_hash=bridge_leading_hash,
            shared_window_end=shared_window_end,
            verdict="comparison_ready_but_not_equivalent",
            note=(
                "Both sides now have explicit positive-index bridge-window hashes, so the target odd-zeta channel can be "
                "compared operationally. They are not claimed equivalent, because the baseline side is not normalized or "
                "derived into the same recurrence-backed object class."
            ),
        ),
        ZudilinBridgeChannelComparison(
            channel_id="companion_channel",
            baseline_object="baseline residual zeta(3) channel from the retained-pair split",
            bridge_object="Zudilin 2002 explicit p̃_n / q_n bridge channel for zeta(3)",
            baseline_window_hash=baseline_companion_hash,
            bridge_window_hash=bridge_companion_hash,
            shared_window_end=shared_window_end,
            verdict="comparison_ready_but_not_equivalent",
            note=(
                "Both sides now have explicit bridge-window hashes for the companion channel, which makes the residual "
                "zeta(3) bookkeeping comparison operational. The baseline side is still residual data only, not a derived "
                "bridge-style companion sequence."
            ),
        ),
    )

    return Zudilin2002BridgeComparisonProbe(
        probe_id="bz_phase2_zudilin_2002_bridge_comparison_probe",
        bridge_id="zudilin_2002_third_order_zeta5_bridge",
        shared_window_start=1,
        shared_window_end=shared_window_end,
        channel_comparisons=channel_comparisons,
        overall_verdict=(
            "The external bridge comparison is now operational on a real shared window. The baseline and Zudilin 2002 "
            "channels can be compared as explicit hashed objects for n=1..7, but the comparison remains intentionally "
            "non-equivalence-based because the sequence-strength gap is still unresolved."
        ),
        next_step=(
            "If we continue on this line, the next meaningful move is to design one explicit normalization map candidate "
            "from the baseline retained zeta(5) channel toward the Zudilin bridge shape and test it on the shared window."
        ),
    )


def render_zudilin_2002_bridge_comparison_probe(*, max_n: int = 7) -> str:
    probe = build_zudilin_2002_bridge_comparison_probe(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 bridge comparison probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Bridge probe: `{ZUDILIN_2002_BRIDGE_REPORT_PATH}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Bridge id: `{probe.bridge_id}`",
        "",
        "| channel | baseline window hash | bridge window hash | verdict |",
        "| --- | --- | --- | --- |",
    ]
    for item in probe.channel_comparisons:
        lines.append(
            f"| `{item.channel_id}` | `{item.baseline_window_hash}` | `{item.bridge_window_hash}` | `{item.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
        ]
    )
    for item in probe.channel_comparisons:
        lines.append(f"- `{item.channel_id}`: {item.note}")
    lines.extend(
        [
            "",
            "## Overall verdict",
            "",
            probe.overall_verdict,
            "",
            "## Next step",
            "",
            probe.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_zudilin_2002_bridge_comparison_probe_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_BRIDGE_COMPARISON_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_bridge_comparison_probe(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_bridge_comparison_probe_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_BRIDGE_COMPARISON_JSON_PATH,
) -> Path:
    probe = build_zudilin_2002_bridge_comparison_probe(max_n=max_n)
    payload = {
        "probe_id": probe.probe_id,
        "bridge_id": probe.bridge_id,
        "shared_window_start": probe.shared_window_start,
        "shared_window_end": probe.shared_window_end,
        "channel_comparisons": [asdict(item) for item in probe.channel_comparisons],
        "overall_verdict": probe.overall_verdict,
        "next_step": probe.next_step,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def _provisional_hash(*, component_id: str, signature: tuple) -> str:
    identity = ProvisionalSequenceIdentity.from_scalars(
        start_index=1,
        order_bound=max(1, len(signature) - 1),
        initial_data=signature[: min(2, len(signature))],
        signature=signature,
    )
    return compute_provisional_sequence_hash(identity)


def _extract_sample_fraction(text: str):
    from fractions import Fraction

    return Fraction(text)


def main() -> None:
    write_zudilin_2002_bridge_comparison_probe_report()
    write_zudilin_2002_bridge_comparison_probe_json()


if __name__ == "__main__":
    main()
