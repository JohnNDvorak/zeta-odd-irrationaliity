from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .external_bridge_comparison_target import (
    EXTERNAL_BRIDGE_COMPARISON_REPORT_PATH,
    build_phase2_external_bridge_comparison_target,
)
from .external_bridge_spec import EXTERNAL_BRIDGE_SPEC_REPORT_PATH

EXTERNAL_BRIDGE_COMPARISON_PROBE_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_external_bridge_comparison_probe.md"
EXTERNAL_BRIDGE_COMPARISON_PROBE_JSON_PATH = CACHE_DIR / "bz_phase2_external_bridge_comparison_probe.json"


@dataclass(frozen=True)
class BridgeProbeFieldVerdict:
    field_id: str
    baseline_strength: str
    bridge_strength: str
    verdict: str
    explanation: str


@dataclass(frozen=True)
class ExternalBridgeComparisonProbe:
    probe_id: str
    bridge_id: str
    aligned_fields: tuple[str, ...]
    partial_fields: tuple[str, ...]
    blocking_fields: tuple[str, ...]
    field_verdicts: tuple[BridgeProbeFieldVerdict, ...]
    overall_verdict: str
    next_step: str


def build_phase2_external_bridge_comparison_probe() -> ExternalBridgeComparisonProbe:
    target = build_phase2_external_bridge_comparison_target()
    verdicts = []
    aligned_fields: list[str] = []
    partial_fields: list[str] = []
    blocking_fields: list[str] = []

    for field in target.comparison_fields:
        if field.field_id in {"leading_target_channel", "companion_channel"}:
            verdict = "structurally_partial"
            partial_fields.append(field.field_id)
            baseline_strength = "explicit hashed coefficient-side object"
            bridge_strength = "published recurrence-backed linear-form channel"
            explanation = (
                "The baseline side is good enough to support channel-level comparison because the channel is explicit, "
                "hashed, and not hidden. It still falls short of the bridge object because it has not yet been promoted "
                "to a published-style recurrence-backed linear form."
            )
        else:
            verdict = "blocking_gap"
            blocking_fields.append(field.field_id)
            baseline_strength = "finite exact windows only"
            bridge_strength = "recurrence plus initial data"
            explanation = (
                "This remains the main blocker. The baseline side is reproducible only on shared finite windows, while "
                "the bridge object is sequence-explicit. Until that asymmetry is either reduced or deliberately accepted, "
                "the comparison cannot be stronger than structural."
            )
        verdicts.append(
            BridgeProbeFieldVerdict(
                field_id=field.field_id,
                baseline_strength=baseline_strength,
                bridge_strength=bridge_strength,
                verdict=verdict,
                explanation=explanation,
            )
        )

    overall_verdict = (
        "The external bridge comparison is now concrete enough to be useful: two fields are structurally partial matches "
        "and one field is the clear blocker. That means the next productive artifact should not be another abstract spec. "
        "It should be a comparison note that explicitly accepts the finite-window asymmetry and then states one normalization-level "
        "comparison against Zudilin 2002."
    )

    return ExternalBridgeComparisonProbe(
        probe_id="bz_phase2_external_bridge_comparison_probe",
        bridge_id=target.bridge_id,
        aligned_fields=tuple(aligned_fields),
        partial_fields=tuple(partial_fields),
        blocking_fields=tuple(blocking_fields),
        field_verdicts=tuple(verdicts),
        overall_verdict=overall_verdict,
        next_step=(
            "Write a normalization-level comparison note for the Zudilin 2002 bridge that explicitly compares the baseline "
            "retained `(constant, ζ(5))` pair and residual `ζ(3)` channel to the published bridge channels while accepting "
            "that the baseline side is finite-window rather than recurrence-explicit."
        ),
    )


def render_phase2_external_bridge_comparison_probe() -> str:
    probe = build_phase2_external_bridge_comparison_probe()
    lines = [
        "# Phase 2 external bridge comparison probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Bridge target report: `{EXTERNAL_BRIDGE_COMPARISON_REPORT_PATH}`",
        f"- Bridge spec report: `{EXTERNAL_BRIDGE_SPEC_REPORT_PATH}`",
        f"- Bridge id: `{probe.bridge_id}`",
        f"- Partial fields: `{', '.join(probe.partial_fields)}`",
        f"- Blocking fields: `{', '.join(probe.blocking_fields)}`",
        "",
        "## Field verdicts",
        "",
        "| field | baseline strength | bridge strength | verdict |",
        "| --- | --- | --- | --- |",
    ]
    for verdict in probe.field_verdicts:
        lines.append(
            f"| `{verdict.field_id}` | {verdict.baseline_strength} | {verdict.bridge_strength} | `{verdict.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Explanations",
            "",
        ]
    )
    for verdict in probe.field_verdicts:
        lines.append(f"- `{verdict.field_id}`: {verdict.explanation}")
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


def write_phase2_external_bridge_comparison_probe_report(
    output_path: str | Path = EXTERNAL_BRIDGE_COMPARISON_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_bridge_comparison_probe(), encoding="utf-8")
    return output


def write_phase2_external_bridge_comparison_probe_json(
    output_path: str | Path = EXTERNAL_BRIDGE_COMPARISON_PROBE_JSON_PATH,
) -> Path:
    probe = build_phase2_external_bridge_comparison_probe()
    payload = {
        "probe_id": probe.probe_id,
        "bridge_id": probe.bridge_id,
        "aligned_fields": list(probe.aligned_fields),
        "partial_fields": list(probe.partial_fields),
        "blocking_fields": list(probe.blocking_fields),
        "field_verdicts": [asdict(item) for item in probe.field_verdicts],
        "overall_verdict": probe.overall_verdict,
        "next_step": probe.next_step,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_bridge_comparison_probe_report()
    write_phase2_external_bridge_comparison_probe_json()


if __name__ == "__main__":
    main()
