from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_source_packet_probe import (
    SYMMETRIC_SOURCE_PACKET_PROBE_REPORT_PATH,
    build_symmetric_source_packet_probe,
)

SYMMETRIC_SOURCE_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_source_packet_post_probe_decision_gate.md"
)
SYMMETRIC_SOURCE_PACKET_POST_PROBE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_source_packet_post_probe_decision_gate.json"
)


@dataclass(frozen=True)
class SymmetricSourcePacketDecisionStatus:
    criterion_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class SymmetricSourcePacketPostProbeDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[SymmetricSourcePacketDecisionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    non_claims: tuple[str, ...]


def build_symmetric_source_packet_post_probe_decision_gate() -> SymmetricSourcePacketPostProbeDecisionGate:
    probe = build_symmetric_source_packet_probe()
    return SymmetricSourcePacketPostProbeDecisionGate(
        gate_id="bz_phase2_symmetric_source_packet_post_probe_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=(
            SymmetricSourcePacketDecisionStatus(
                criterion_id="source_backed_scaled_packet",
                verdict="satisfied",
                note="The packet is source-backed and respects the published arithmetic scales.",
            ),
            SymmetricSourcePacketDecisionStatus(
                criterion_id="reproducible_hash",
                verdict="satisfied",
                note="The packet is reproducible via an exact packet hash on n=1..80.",
            ),
            SymmetricSourcePacketDecisionStatus(
                criterion_id="pairwise_neutrality",
                verdict="satisfied",
                note="No pairwise compression route has been privileged before exact testing.",
            ),
            SymmetricSourcePacketDecisionStatus(
                criterion_id="compression_choice",
                verdict="not_yet_satisfied",
                note="No low-complexity residual orientation has been certified or closed yet inside the symmetric source family.",
            ),
        ),
        outcome="continue_symmetric_source_packet_compression",
        rationale=(
            "The scaled symmetric source packet is strong enough to justify one bounded pairwise compression layer. "
            "That layer should test all three residual orientations with the fixed low-complexity families already used elsewhere in phase 2."
        ),
        next_step=(
            "Implement the symmetric source packet compression probe and decision gate. Do not jump to richer ansatz families before this bounded layer is closed."
        ),
        non_claims=(
            "This does not claim a baseline transfer.",
            "This does not claim the symmetric source family already determines a baseline remainder object.",
            "This does not justify skipping the symmetric source compression gate.",
        ),
    )


def render_symmetric_source_packet_post_probe_decision_gate() -> str:
    gate = build_symmetric_source_packet_post_probe_decision_gate()
    lines = [
        "# Phase 2 symmetric source packet post-probe decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SYMMETRIC_SOURCE_PACKET_PROBE_REPORT_PATH}`",
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


def write_symmetric_source_packet_post_probe_decision_gate_report(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_source_packet_post_probe_decision_gate(), encoding="utf-8")
    return output


def write_symmetric_source_packet_post_probe_decision_gate_json(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_POST_PROBE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_symmetric_source_packet_post_probe_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_source_packet_post_probe_decision_gate_report()
    write_symmetric_source_packet_post_probe_decision_gate_json()


if __name__ == "__main__":
    main()
