from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_source_packet_compression_probe import (
    SYMMETRIC_SOURCE_PACKET_COMPRESSION_PROBE_REPORT_PATH,
    build_symmetric_source_packet_compression_probe,
)

SYMMETRIC_SOURCE_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_source_packet_compression_decision_gate.md"
)
SYMMETRIC_SOURCE_PACKET_COMPRESSION_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_source_packet_compression_decision_gate.json"
)


@dataclass(frozen=True)
class SymmetricSourcePacketCompressionStatus:
    route_id: str
    route_verdict: str
    note: str


@dataclass(frozen=True)
class SymmetricSourcePacketCompressionDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[SymmetricSourcePacketCompressionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    source_boundary: str


def build_symmetric_source_packet_compression_decision_gate() -> SymmetricSourcePacketCompressionDecisionGate:
    probe = build_symmetric_source_packet_compression_probe()
    all_closed = all(item.route_verdict.startswith("hard_wall") for item in probe.route_results)
    return SymmetricSourcePacketCompressionDecisionGate(
        gate_id="bz_phase2_symmetric_source_packet_compression_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=tuple(
            SymmetricSourcePacketCompressionStatus(
                route_id=item.route_id,
                route_verdict=item.route_verdict,
                note=(
                    "Closed by an exact full-window failure of the fixed low-complexity ladder."
                    if item.route_verdict.startswith("hard_wall")
                    else "Still open because at least one fixed low-complexity family survives on the full validation window."
                ),
            )
            for item in probe.route_results
        ),
        outcome=(
            "hard_wall_symmetric_source_pairwise_compression_exhausted"
            if all_closed
            else "continue_symmetric_source_pairwise_compression_winner"
        ),
        rationale=(
            "All three pairwise low-complexity compression routes for the scaled totally symmetric source packet are now closed."
            if all_closed
            else "At least one pairwise low-complexity compression route remains open inside the scaled totally symmetric source packet."
        ),
        next_step=(
            "Stop autonomous execution and ask the user for the next pivot."
            if all_closed
            else "Continue on the surviving symmetric source packet compression route."
        ),
        pivot_options=(
            "richer_symmetric_source_family",
            "symmetric_to_baseline_transfer_path",
        ),
        source_boundary=probe.source_boundary,
    )


def render_symmetric_source_packet_compression_decision_gate() -> str:
    gate = build_symmetric_source_packet_compression_decision_gate()
    lines = [
        "# Phase 2 symmetric source packet compression decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SYMMETRIC_SOURCE_PACKET_COMPRESSION_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| route | verdict | note |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.route_id}` | `{item.route_verdict}` | {item.note} |")
    lines.extend(
        [
            "",
            "## Rationale",
            "",
            gate.rationale,
            "",
            "## Next step",
            "",
            gate.next_step,
            "",
            "## Source boundary",
            "",
            gate.source_boundary,
            "",
            "## Pivot options",
            "",
        ]
    )
    for item in gate.pivot_options:
        lines.append(f"- `{item}`")
    lines.append("")
    return "\n".join(lines)


def write_symmetric_source_packet_compression_decision_gate_report(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_source_packet_compression_decision_gate(), encoding="utf-8")
    return output


def write_symmetric_source_packet_compression_decision_gate_json(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_COMPRESSION_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_symmetric_source_packet_compression_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_source_packet_compression_decision_gate_report()
    write_symmetric_source_packet_compression_decision_gate_json()


if __name__ == "__main__":
    main()
