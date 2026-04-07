from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .gate0_parse import run_gate0
from .gate1_filter import run_gate1
from .sequence_evidence import resolve_candidate_sequence_evidence
from .storage import append_result, save_candidate_snapshot

MODE_CHOICES = ("Mode A-fast", "Mode A-slow", "Mode B")


def build_structural_payload(*, candidate_path: Path) -> tuple[dict[str, Any], int]:
    gate0 = run_gate0(candidate_path)
    gate1 = run_gate1(gate0)
    candidate, evidence = resolve_candidate_sequence_evidence(gate0.candidate)

    payload = {
        "candidate": candidate.to_display_dict(),
        "gate0": {
            "canonicalized": gate0.canonicalized,
            "canonicalization_permutation": list(gate0.canonicalization_permutation),
        },
        "gate1": {
            "accepted": gate1.accepted,
            "errors": list(gate1.errors),
            "warnings": list(gate1.warnings),
            "parity_failures": list(gate1.parity.failures),
            "convergence_failures": list(gate1.convergence.failures),
        },
    }
    if evidence is not None:
        payload["sequence_evidence"] = evidence.to_metadata()
    return payload, (0 if gate1.accepted else 1)


def log_structural_run(
    *,
    candidate_path: Path,
    mode: str = "",
    notes: str = "",
    snapshot_root: Path | None = None,
    results_path: Path | None = None,
) -> dict[str, str]:
    gate0 = run_gate0(candidate_path)
    gate1 = run_gate1(gate0)
    candidate, evidence = resolve_candidate_sequence_evidence(gate0.candidate)
    snapshot_path = save_candidate_snapshot(
        candidate,
        root=snapshot_root if snapshot_root is not None else None,
        extra_payload={
            "gate1": {
                "accepted": gate1.accepted,
                "errors": list(gate1.errors),
                "warnings": list(gate1.warnings),
            },
            "sequence_evidence": None if evidence is None else evidence.to_metadata(),
        },
    )
    status = "" if gate1.accepted else "invalidated"
    result_path = append_result(
        {
            "id": candidate.id or candidate.routing_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "configuration_label": candidate.configuration.label,
            "family_label": candidate.configuration.family_label,
            "routing_hash": candidate.routing_hash,
            "sequence_hash": candidate.sequence_hash,
            "certificate_hash": candidate.certificate_hash,
            "mode": mode,
            "representation": candidate.representation.presentation,
            "certificate_template": candidate.certificate.template,
            "certification_status": status,
            "u": candidate.affine_family.to_hashable_payload()["u"],
            "v": candidate.affine_family.to_hashable_payload()["v"],
            "gate_reached": "gate1",
            "equality_witness": candidate.representation.equality_witness,
            "notes": _combine_notes(
                gate1=gate1.accepted,
                notes=notes,
                evidence_note="" if evidence is None else f"sequence_evidence={evidence.id}; sequence_hash_status={evidence.sequence_hash_status}",
            ),
        },
        path=results_path if results_path is not None else None,
    )
    return {
        "candidate_snapshot": str(snapshot_path),
        "results_path": str(result_path),
    }


def _combine_notes(*, gate1: bool, notes: str, evidence_note: str = "") -> str:
    prefix = "structural_gate1_accept" if gate1 else "structural_gate1_reject"
    parts = [prefix]
    if evidence_note:
        parts.append(evidence_note)
    if notes:
        parts.append(notes)
    return "; ".join(parts)

def main() -> int:
    parser = argparse.ArgumentParser(description="Run Gate 0 and Gate 1 for a zeta(5) candidate spec.")
    parser.add_argument("candidate", type=Path, help="Path to a YAML candidate spec")
    parser.add_argument("--log", action="store_true", help="Archive the canonical candidate snapshot and append a Gate 1 result row.")
    parser.add_argument("--mode", choices=MODE_CHOICES, default="", help="Intended downstream mode for the candidate.")
    parser.add_argument("--notes", default="", help="Extra notes to append to the dry-run ledger row.")
    args = parser.parse_args()

    payload, exit_code = build_structural_payload(candidate_path=args.candidate)
    if args.log:
        payload["logging"] = log_structural_run(candidate_path=args.candidate, mode=args.mode, notes=args.notes)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
