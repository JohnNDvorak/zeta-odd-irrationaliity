from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_full_packet_probe import (
    BASELINE_FULL_PACKET_PROBE_REPORT_PATH,
    build_baseline_full_packet_probe,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_FULL_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_full_packet_post_probe_decision_gate.md"
)
BASELINE_FULL_PACKET_POST_PROBE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_full_packet_post_probe_decision_gate.json"
)


@dataclass(frozen=True)
class BaselineFullPacketDecisionStatus:
    criterion_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class BaselineFullPacketPostProbeDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[BaselineFullPacketDecisionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    non_claims: tuple[str, ...]


def build_baseline_full_packet_post_probe_decision_gate() -> BaselineFullPacketPostProbeDecisionGate:
    probe = build_baseline_full_packet_probe()
    return BaselineFullPacketPostProbeDecisionGate(
        gate_id="bz_phase2_baseline_full_packet_post_probe_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=(
            BaselineFullPacketDecisionStatus(
                criterion_id="baseline_native_packet",
                verdict="satisfied",
                note="The probe establishes a baseline-native full packet rather than a chosen pair surrogate.",
            ),
            BaselineFullPacketDecisionStatus(
                criterion_id="reproducible_hash",
                verdict="satisfied",
                note="The full packet is reproducible via an exact packet hash.",
            ),
            BaselineFullPacketDecisionStatus(
                criterion_id="pairwise_neutrality",
                verdict="satisfied",
                note="The object does not privilege one pairwise compression route before exact testing.",
            ),
            BaselineFullPacketDecisionStatus(
                criterion_id="compression_choice",
                verdict="not_yet_satisfied",
                note="No pairwise compression route has been certified or closed yet for the full packet object.",
            ),
        ),
        outcome="continue_full_packet_compression",
        rationale=(
            "The full packet probe is strong enough to justify one bounded pairwise compression layer. That layer should "
            "use the two prior hard-wall gates plus one new zeta(5)-residual route to close the packet-level low-complexity space."
        ),
        next_step=(
            "Implement the full-packet compression probe and decision gate. It should aggregate the two prior hard-wall routes and one new zeta(5)-residual route."
        ),
        non_claims=(
            "This does not claim a baseline `P_n` extraction.",
            "This does not claim a proved baseline remainder pipeline.",
            "This does not justify skipping the packet-level compression gate.",
        ),
    )


def render_baseline_full_packet_post_probe_decision_gate() -> str:
    gate = build_baseline_full_packet_post_probe_decision_gate()
    lines = [
        "# Phase 2 baseline full-packet post-probe decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{BASELINE_FULL_PACKET_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| criterion | verdict | note |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.criterion_id}` | `{item.verdict}` | {item.note} |")
    lines.extend(["", "## Rationale", "", gate.rationale, "", "## Next step", "", gate.next_step, "", "## Non-claims", ""])
    for item in gate.non_claims:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_baseline_full_packet_post_probe_decision_gate_report(
    output_path: str | Path = BASELINE_FULL_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_full_packet_post_probe_decision_gate(), encoding="utf-8")
    return output


def write_baseline_full_packet_post_probe_decision_gate_json(
    output_path: str | Path = BASELINE_FULL_PACKET_POST_PROBE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_baseline_full_packet_post_probe_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_full_packet_post_probe_decision_gate_report()
    write_baseline_full_packet_post_probe_decision_gate_json()


if __name__ == "__main__":
    main()
