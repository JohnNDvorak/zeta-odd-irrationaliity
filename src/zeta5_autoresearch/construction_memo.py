from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_decay_audit import (
    CHECKPOINT_REPORT_PATH,
    PIVOT_REPORT_PATH,
    build_phase2_baseline_decay_audit,
    build_phase2_dual_companion_checkpoint,
    build_phase2_pivot_decision,
)
from .baseline_decay_bridge import (
    BRIDGE_REPORT_PATH,
    build_phase2_baseline_decay_bridge,
)
from .config import CACHE_DIR, DATA_DIR
from .literature_verification import (
    LITERATURE_VERIFICATION_REPORT_PATH,
    build_phase2_literature_claims,
)

CONSTRUCTION_MEMO_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_construction_memo.md"
CONSTRUCTION_MEMO_JSON_PATH = CACHE_DIR / "bz_phase2_construction_memo.json"


@dataclass(frozen=True)
class ConstructionPath:
    path_id: str
    title: str
    objective: str
    supporting_sources: tuple[str, ...]
    existing_assets: tuple[str, ...]
    blocking_gap: str
    payoff: str
    risk: str
    recommendation: str


@dataclass(frozen=True)
class ConstructionMemo:
    memo_id: str
    baseline_seed: str
    executive_verdict: str
    banked_assets: tuple[str, ...]
    missing_objects: tuple[str, ...]
    construction_paths: tuple[ConstructionPath, ...]
    next_step: str


def build_phase2_construction_memo() -> ConstructionMemo:
    claims = build_phase2_literature_claims()
    checkpoint = build_phase2_dual_companion_checkpoint()
    audit = build_phase2_baseline_decay_audit()
    bridge = build_phase2_baseline_decay_bridge()
    pivot = build_phase2_pivot_decision()

    baseline_gap_confirmed = any(
        claim.verdict == "not found"
        and claim.source == "Brown-Zudilin, arXiv:2210.03391v3"
        and claim.applies_to == "baseline specialization"
        for claim in claims
    )
    symmetric_anchor_confirmed = any(
        claim.verdict == "confirmed"
        and claim.source == "Brown-Zudilin, arXiv:2210.03391v3"
        and claim.applies_to == "totally symmetric specialization"
        for claim in claims
    )

    if not baseline_gap_confirmed or not symmetric_anchor_confirmed:
        raise ValueError("Construction memo requires the verified baseline-gap and symmetric-anchor claims.")

    banked_assets = (
        (
            "Verified literature result: Brown-Zudilin v3 explicitly publishes the totally symmetric "
            "Brown-Zudilin specialization as a sequence-level anchor but no checked explicit baseline non-symmetric P_n / recurrence for "
            "a=(8,16,10,15,12,16,18,13)."
        ),
        (
            "Frozen dual-companion checkpoint: exact baseline dual constant and zeta(3) companion caches "
            f"banked through n={checkpoint.constant_cache_max_n} and n={checkpoint.zeta3_cache_max_n}."
        ),
        (
            "Certified exclusion artifact: baseline dual companion sequences have no nontrivial "
            f"(1,0,-1,-2) polynomial recurrence through degree {checkpoint.certified_degree} on the exact "
            f"window n<={checkpoint.certified_window_max_n}."
        ),
        (
            "Repo-native calibration anchor: the totally symmetric remainder pipeline is source-backed, "
            f"normalized through the generic decay-probe interface, and currently verified through "
            f"n={audit.symmetric_decay_probe.max_verified_index}."
        ),
        (
            "Bridge literature: explicit external zeta(5) linear-form constructions exist in Zudilin 2002 "
            "and Zudilin 2018, plus denominator-side cellular and motivic/parity bridges in "
            "McCarthy-Osburn-Straub 2020, Dupont 2018, and Tosi 2026."
        ),
    )

    missing_objects = (
        "No checked explicit baseline non-symmetric P_n sequence for a=(8,16,10,15,12,16,18,13).",
        "No checked explicit baseline non-symmetric recurrence analogous to the symmetric Section 2 recurrence.",
        "No checked direct baseline remainder fixture that can be ingested into the generic decay-probe pipeline.",
    )

    construction_paths = (
        ConstructionPath(
            path_id="baseline_dual_projection_path",
            title="Dual cellular projection path",
            objective=(
                "Turn the Brown-Zudilin generalized baseline family itself into explicit coefficient data by "
                "combining the dual-cellular perspective with a coefficient/parity projection mechanism."
            ),
            supporting_sources=(
                "Brown-Zudilin, arXiv:2210.03391v3",
                "Brown, Irrationality proofs, moduli spaces and dinner parties (2014 notes)",
                "Dupont, Odd zeta motive and linear forms in odd zeta values (2018)",
            ),
            existing_assets=(
                "Exact dual F7 coefficient extraction infrastructure in the repo.",
                "Frozen dual companion caches and exclusion report.",
                "Generic decay-probe and baseline readiness-bridge reports.",
            ),
            blocking_gap=(
                "No published coefficient-extraction algorithm specialized to the Brown-Zudilin baseline seed; "
                "the projection step must be constructed rather than ingested."
            ),
            payoff=(
                "Highest proof relevance, because success would produce a baseline-family decay object instead "
                "of an external analog."
            ),
            risk=(
                "High mathematical and engineering risk: this is a new extraction build, not a simple transcription "
                "of a published recurrence."
            ),
            recommendation=(
                "Primary construction path once we stop expecting a hidden published baseline P_n formula to appear."
            ),
        ),
        ConstructionPath(
            path_id="hypergeometric_bridge_path",
            title="External hypergeometric bridge comparison path",
            objective=(
                "Use explicit external zeta(5) linear-form constructions as calibration and comparison targets to "
                "infer what kind of coefficient structure the baseline cellular side would need to expose."
            ),
            supporting_sources=(
                "Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)",
                "Zudilin, Arithmetic of linear forms involving odd zeta values (2002)",
                "Zudilin, Some hypergeometric integrals for linear forms in zeta values (2018)",
            ),
            existing_assets=(
                "Verified literature report already identifies these as explicit external decay-side bridge objects.",
                "Repo has exact dual-side coefficient extraction machinery and sequence identity infrastructure.",
            ),
            blocking_gap=(
                "This path does not directly solve the Brown-Zudilin baseline problem; it only constrains or "
                "suggests candidate extraction shapes."
            ),
            payoff=(
                "Moderate payoff with lower risk: it can sharpen target invariants and provide implementation tests "
                "without first solving the full baseline projection problem."
            ),
            risk=(
                "Risk of overfitting to neighboring zeta(5) constructions that are structurally different from the "
                "generalized cellular baseline."
            ),
            recommendation=(
                "Best secondary path and the safest place to prototype extraction logic before applying it to the baseline family."
            ),
        ),
        ConstructionPath(
            path_id="cellular_contiguity_path",
            title="Generalized cellular contiguity / denominator-side reconstruction path",
            objective=(
                "Reconstruct explicit baseline coefficient data from the generalized cellular family using the "
                "baseline matrix, denominator-side cellular analogs, and any recoverable contiguity structure."
            ),
            supporting_sources=(
                "Brown-Zudilin, arXiv:2210.03391v3",
                "McCarthy-Osburn-Straub, Sequences, modular forms and cellular integrals (2020)",
                "Tosi, An explicit study of a family of cellular integrals (2026)",
                "Tosi, dissertation / reflection-arrangement framework (2026)",
            ),
            existing_assets=(
                "Repo has baseline Q_n infrastructure, modular recurrence scanners, and the verified baseline matrix reference.",
                "Literature report now separates basic-cellular denominator-side results from the missing generalized baseline decay object.",
            ),
            blocking_gap=(
                "No checked published contiguity package for the generalized non-symmetric baseline seed; "
                "the needed coefficient-recovery mechanism is still implicit."
            ),
            payoff=(
                "Potentially high if a workable contiguity relation is found, because it would stay closest to the "
                "actual Brown-Zudilin baseline family."
            ),
            risk=(
                "High risk of large symbolic complexity and of reproducing the same exact-arithmetic bottlenecks in a new guise."
            ),
            recommendation=(
                "Promising only after the literature-backed projection and bridge routes are clearly exhausted or better specified."
            ),
        ),
    )

    next_step = (
        "Treat the literature search as saturated enough to stop broadening it. Keep the current baseline readiness "
        f"bridge (`{bridge.bridge_id}`) and pivot outcome (`{pivot.outcome}`), then begin a bounded construction "
        "program on the dual cellular projection path, using the external hypergeometric bridge path as calibration."
    )

    return ConstructionMemo(
        memo_id="bz_phase2_construction_memo",
        baseline_seed="a=(8,16,10,15,12,16,18,13)",
        executive_verdict=(
            "The verified literature supports a sharp split: the totally symmetric Brown-Zudilin specialization is "
            "sequence-explicit, while the Brown-Zudilin baseline non-symmetric seed is asymptotic/arithmetic but not "
            "sequence-explicit in the checked sources. The next honest move is no longer source hunting; it is a "
            "construction program that uses the verified bridges to build a baseline decay-side extraction path."
        ),
        banked_assets=banked_assets,
        missing_objects=missing_objects,
        construction_paths=construction_paths,
        next_step=next_step,
    )


def render_phase2_construction_memo() -> str:
    memo = build_phase2_construction_memo()
    lines = [
        "# Phase 2 construction memo",
        "",
        f"- Memo id: `{memo.memo_id}`",
        f"- Baseline seed: `{memo.baseline_seed}`",
        f"- Literature verification report: `{LITERATURE_VERIFICATION_REPORT_PATH}`",
        f"- Frozen checkpoint report: `{CHECKPOINT_REPORT_PATH}`",
        f"- Readiness bridge report: `{BRIDGE_REPORT_PATH}`",
        f"- Pivot report: `{PIVOT_REPORT_PATH}`",
        "",
        "## Executive verdict",
        "",
        memo.executive_verdict,
        "",
        "## Banked assets",
        "",
    ]
    for asset in memo.banked_assets:
        lines.append(f"- {asset}")
    lines.extend(
        [
            "",
            "## Missing objects",
            "",
        ]
    )
    for item in memo.missing_objects:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Construction paths",
            "",
        ]
    )
    for path in memo.construction_paths:
        lines.extend(
            [
                f"### {path.title}",
                "",
                f"- Path id: `{path.path_id}`",
                f"- Objective: {path.objective}",
                f"- Supporting sources: {', '.join(f'`{source}`' for source in path.supporting_sources)}",
                f"- Existing assets: {' '.join(f'`{asset}`' for asset in path.existing_assets)}",
                f"- Blocking gap: {path.blocking_gap}",
                f"- Payoff: {path.payoff}",
                f"- Risk: {path.risk}",
                f"- Recommendation: {path.recommendation}",
                "",
            ]
        )
    lines.extend(
        [
            "## Recommended next step",
            "",
            memo.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_construction_memo_report(
    output_path: str | Path = CONSTRUCTION_MEMO_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_construction_memo(), encoding="utf-8")
    return output


def write_phase2_construction_memo_json(
    output_path: str | Path = CONSTRUCTION_MEMO_JSON_PATH,
) -> Path:
    memo = build_phase2_construction_memo()
    payload = {
        "memo_id": memo.memo_id,
        "baseline_seed": memo.baseline_seed,
        "executive_verdict": memo.executive_verdict,
        "banked_assets": list(memo.banked_assets),
        "missing_objects": list(memo.missing_objects),
        "construction_paths": [asdict(path) for path in memo.construction_paths],
        "next_step": memo.next_step,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_construction_memo_report()
    write_phase2_construction_memo_json()


if __name__ == "__main__":
    main()
