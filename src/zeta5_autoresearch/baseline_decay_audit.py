from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

from .config import CACHE_DIR, DATA_DIR, REPO_ROOT
from .decay_probe import DecayProbeSummary, build_missing_decay_probe_summary
from .dual_f7_exact_coefficient_cache import (
    BASELINE_DUAL_F7_CONSTANT_CACHE_PATH,
    BASELINE_DUAL_F7_ZETA3_CACHE_PATH,
)
from .bz_symmetric_linear_forms_probe import build_bz_totally_symmetric_linear_forms_probe

CATALOG_PATH = REPO_ROOT / "regression" / "fixtures" / "bz_phase2_local_object_catalog.yaml"
DUAL_COMPANION_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_companion_normalization_report.md"
CHECKPOINT_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_dual_companion_checkpoint.md"
AUDIT_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_baseline_decay_audit_report.md"
AUDIT_JSON_PATH = CACHE_DIR / "bz_phase2_baseline_decay_audit.json"
PIVOT_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_pivot_report.md"


@dataclass(frozen=True)
class ResearchObjectCatalogEntry:
    object_id: str
    family: str
    object_kind: str
    source_status: str
    exact_status: str
    local_source_path: str
    current_ingestion_path: str
    max_verified_index: int | None
    proof_relevance: str
    notes: str


@dataclass(frozen=True)
class DualCompanionCheckpoint:
    constant_cache_max_n: int
    zeta3_cache_max_n: int
    certified_window_max_n: int
    certified_degree: int
    certified_rank: int
    reopen_criterion: str


@dataclass(frozen=True)
class BaselineDecayAudit:
    catalog: tuple[ResearchObjectCatalogEntry, ...]
    symmetric_decay_probe: DecayProbeSummary
    baseline_decay_placeholder: DecayProbeSummary


@dataclass(frozen=True)
class PivotDecision:
    outcome: str
    rationale: str


def load_phase2_local_object_catalog(path: str | Path = CATALOG_PATH) -> tuple[ResearchObjectCatalogEntry, ...]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    rows = payload["phase2_local_object_catalog"]["objects"]
    entries = tuple(
        ResearchObjectCatalogEntry(
            object_id=str(row["object_id"]),
            family=str(row["family"]),
            object_kind=str(row["object_kind"]),
            source_status=str(row["source_status"]),
            exact_status=str(row["exact_status"]),
            local_source_path=str(row["local_source_path"]),
            current_ingestion_path=str(row["current_ingestion_path"]),
            max_verified_index=(None if row.get("max_verified_index") is None else int(row["max_verified_index"])),
            proof_relevance=str(row["proof_relevance"]),
            notes=str(row["notes"]),
        )
        for row in rows
    )
    return tuple(_with_live_max_verified_index(entry) for entry in entries)


def build_phase2_dual_companion_checkpoint(
    report_path: str | Path = DUAL_COMPANION_REPORT_PATH,
    constant_cache_path: str | Path = BASELINE_DUAL_F7_CONSTANT_CACHE_PATH,
    zeta3_cache_path: str | Path = BASELINE_DUAL_F7_ZETA3_CACHE_PATH,
) -> DualCompanionCheckpoint:
    report = Path(report_path).read_text(encoding="utf-8")
    certified_window_max_n = _extract_int(report, r"Exact baseline companion sequences loaded through `n=(\d+)`")
    certified_degree = _extract_int(report, r"\| (\d+) \| 428 \| 428 \| 428 \| 0 \|")
    certified_rank = _extract_int(report, r"\| " + str(certified_degree) + r" \| 428 \| 428 \| (\d+) \| 0 \|")
    constant_cache_max_n = _load_cache_max_n(Path(constant_cache_path))
    zeta3_cache_max_n = _load_cache_max_n(Path(zeta3_cache_path))
    return DualCompanionCheckpoint(
        constant_cache_max_n=constant_cache_max_n,
        zeta3_cache_max_n=zeta3_cache_max_n,
        certified_window_max_n=certified_window_max_n,
        certified_degree=certified_degree,
        certified_rank=certified_rank,
        reopen_criterion=(
            "Reopen only if the phase-2 pivot report finds no better repo-local proof-relevant decay path "
            "or if a true representation rewrite is explicitly prioritized."
        ),
    )


def render_phase2_dual_companion_checkpoint_report() -> str:
    checkpoint = build_phase2_dual_companion_checkpoint()
    lines = [
        "# Phase 2 dual-companion checkpoint",
        "",
        "- Status: frozen checkpoint, not the active main line.",
        f"- Baseline dual constant cache banked through `n={checkpoint.constant_cache_max_n}`.",
        f"- Baseline dual `zeta(3)` cache banked through `n={checkpoint.zeta3_cache_max_n}`.",
        f"- Latest certified dual-companion exact window: `n<={checkpoint.certified_window_max_n}`.",
        f"- Latest certified recurrence exclusion: shifts `(1, 0, -1, -2)` through degree `{checkpoint.certified_degree}`.",
        f"- Rank at the frontier degree: `{checkpoint.certified_rank}/428`.",
        "- Why frozen: the remaining `n=435` step is blocked by architectural exact-arithmetic costs in the mixed fraction-pair / `mpq` kernel, while the mathematical value of one more degree step is now lower than the cost.",
        f"- Reopen criterion: {checkpoint.reopen_criterion}",
        "",
        "This checkpoint preserves the exact cached dual companion data and the certified exclusion result as a reusable artifact for future representation rewrites.",
        "",
    ]
    return "\n".join(lines)


def write_phase2_dual_companion_checkpoint_report(output_path: str | Path = CHECKPOINT_REPORT_PATH) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_dual_companion_checkpoint_report(), encoding="utf-8")
    return output


def build_phase2_baseline_decay_audit() -> BaselineDecayAudit:
    catalog = load_phase2_local_object_catalog()
    symmetric_probe = build_bz_totally_symmetric_linear_forms_probe(max_n=14, precision=80).decay_summary
    baseline_placeholder = build_missing_decay_probe_summary(
        object_id="baseline_bz_remainder_pipeline",
        family="baseline",
        object_kind="remainder_pipeline",
        bridge_target_family=None,
        provenance_title="Brown and Zudilin, On cellular rational approximations to zeta(5)",
        provenance_url="https://arxiv.org/abs/2210.03391",
        provenance_version="v3",
        missing_prerequisites=(
            "No repo-local baseline P_n formula or recurrence.",
            "No repo-local baseline remainder / linear-form fixture.",
        ),
        recommendation="Keep baseline decay work on the readiness bridge until a source-backed baseline P_n or remainder object is available locally.",
    )
    return BaselineDecayAudit(
        catalog=catalog,
        symmetric_decay_probe=symmetric_probe,
        baseline_decay_placeholder=baseline_placeholder,
    )


def render_phase2_baseline_decay_audit_report() -> str:
    audit = build_phase2_baseline_decay_audit()
    lines = [
        "# Phase 2 baseline decay audit",
        "",
        "| object id | family | kind | source status | exact status | max verified index | proof relevance |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in audit.catalog:
        max_verified = "" if entry.max_verified_index is None else str(entry.max_verified_index)
        lines.append(
            f"| `{entry.object_id}` | `{entry.family}` | `{entry.object_kind}` | `{entry.source_status}` | `{entry.exact_status}` | `{max_verified}` | `{entry.proof_relevance}` |"
        )

    lines.extend(
        [
            "",
            "## Source-backed decay anchor",
            "",
            f"- Object id: `{audit.symmetric_decay_probe.object_id}`",
            f"- Bridge target family: `{audit.symmetric_decay_probe.bridge_target_family}`",
            f"- Exact indices: `{_format_indices(audit.symmetric_decay_probe.exact_indices)}`",
            f"- Numeric indices: `{_format_indices(audit.symmetric_decay_probe.numeric_indices)}`",
        ]
    )
    for metric in audit.symmetric_decay_probe.available_metrics:
        published = "" if metric.published_value is None else f" (published `{metric.published_value:.8f}`)"
        latest = "" if metric.latest_value is None else f"`{metric.latest_value:.8f}`"
        lines.append(f"- Metric `{metric.name}`: latest {latest}{published}.")

    lines.extend(
        [
            "",
            "## Baseline decay gap",
            "",
            f"- Object id: `{audit.baseline_decay_placeholder.object_id}`",
            f"- Missing prerequisites: {', '.join(f'`{item}`' for item in audit.baseline_decay_placeholder.missing_prerequisites)}",
            f"- Recommendation: {audit.baseline_decay_placeholder.recommendation}",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_baseline_decay_audit_report(output_path: str | Path = AUDIT_REPORT_PATH) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_baseline_decay_audit_report(), encoding="utf-8")
    return output


def write_phase2_baseline_decay_audit_json(output_path: str | Path = AUDIT_JSON_PATH) -> Path:
    audit = build_phase2_baseline_decay_audit()
    payload = {
        "catalog": [asdict(item) for item in audit.catalog],
        "symmetric_decay_probe": _serialize_decay_summary(audit.symmetric_decay_probe),
        "baseline_decay_placeholder": _serialize_decay_summary(audit.baseline_decay_placeholder),
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def build_phase2_pivot_decision() -> PivotDecision:
    audit = build_phase2_baseline_decay_audit()
    baseline_decay_rows = tuple(
        entry
        for entry in audit.catalog
        if entry.family == "baseline" and (entry.object_id == "baseline_bz_pn" or "remainder" in entry.object_kind)
    )
    if any(entry.source_status == "source_backed" and entry.exact_status in {"exact", "mixed"} for entry in baseline_decay_rows):
        return PivotDecision(
            outcome="ingest_baseline_decay_object",
            rationale="A repo-local baseline decay-side object is already source-backed and should be ingested next.",
        )
    if any(entry.family == "baseline" and entry.source_status == "derived_local" and entry.exact_status == "exact" for entry in audit.catalog):
        return PivotDecision(
            outcome="build_baseline_decay_readiness_bridge",
            rationale="Only indirect exact baseline dual objects exist locally, so the next honest move is a baseline decay-readiness bridge rather than reopening kernel work.",
        )
    return PivotDecision(
        outcome="reopen_dual_kernel_engineering",
        rationale="No repo-local proof-relevant decay object remains, so kernel work becomes the fallback.",
    )


def render_phase2_pivot_report() -> str:
    checkpoint = build_phase2_dual_companion_checkpoint()
    decision = build_phase2_pivot_decision()
    lines = [
        "# Phase 2 pivot report",
        "",
        "## Frozen checkpoint",
        "",
        f"- Dual companion caches frozen at `n={checkpoint.constant_cache_max_n}` and `n={checkpoint.zeta3_cache_max_n}`.",
        f"- Certified obstruction frozen at `n<={checkpoint.certified_window_max_n}`, degree `{checkpoint.certified_degree}`.",
        "",
        "## Decision",
        "",
        f"- Outcome: `{decision.outcome}`",
        f"- Rationale: {decision.rationale}",
        "",
        "## Queue reset",
        "",
        "- Priority 1: maintain the repo-local proof-object audit.",
        "- Priority 2: extend the generic decay-probe interface from the totally symmetric anchor.",
        "- Priority 3: ingest any repo-local baseline decay object if one becomes available.",
        "- Deferred: the `n=435` dual-companion kernel fight unless this report is superseded by a stronger reason to reopen it.",
        "",
    ]
    return "\n".join(lines)


def write_phase2_pivot_report(output_path: str | Path = PIVOT_REPORT_PATH) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_pivot_report(), encoding="utf-8")
    return output


def write_phase2_pivot_artifacts() -> tuple[Path, Path, Path, Path]:
    checkpoint = write_phase2_dual_companion_checkpoint_report()
    audit_report = write_phase2_baseline_decay_audit_report()
    audit_json = write_phase2_baseline_decay_audit_json()
    pivot_report = write_phase2_pivot_report()
    return checkpoint, audit_report, audit_json, pivot_report


def main() -> None:
    write_phase2_pivot_artifacts()


def _serialize_decay_summary(summary: DecayProbeSummary) -> dict[str, object]:
    return {
        "object_id": summary.object_id,
        "family": summary.family,
        "object_kind": summary.object_kind,
        "bridge_target_family": summary.bridge_target_family,
        "source_status": summary.source_status,
        "exact_status": summary.exact_status,
        "provenance_title": summary.provenance_title,
        "provenance_url": summary.provenance_url,
        "provenance_version": summary.provenance_version,
        "exact_indices": list(summary.exact_indices),
        "numeric_indices": list(summary.numeric_indices),
        "max_verified_index": summary.max_verified_index,
        "available_metrics": [asdict(metric) for metric in summary.available_metrics],
        "missing_prerequisites": list(summary.missing_prerequisites),
        "recommendation": summary.recommendation,
    }


def _format_indices(indices: tuple[int, ...]) -> str:
    if not indices:
        return "[]"
    if len(indices) <= 6:
        return str(list(indices))
    return f"[{indices[0]}, {indices[1]}, ..., {indices[-2]}, {indices[-1]}]"


def _extract_int(text: str, pattern: str) -> int:
    matches = re.findall(pattern, text)
    if not matches:
        raise ValueError(f"pattern not found: {pattern}")
    match = matches[-1]
    return int(match if isinstance(match, str) else match[0])


def _load_cache_max_n(path: Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return int(payload["max_n"])


def _with_live_max_verified_index(entry: ResearchObjectCatalogEntry) -> ResearchObjectCatalogEntry:
    if not entry.local_source_path.startswith("data/cache/"):
        return entry
    path = REPO_ROOT / entry.local_source_path
    if not path.exists():
        return entry
    return ResearchObjectCatalogEntry(
        object_id=entry.object_id,
        family=entry.family,
        object_kind=entry.object_kind,
        source_status=entry.source_status,
        exact_status=entry.exact_status,
        local_source_path=entry.local_source_path,
        current_ingestion_path=entry.current_ingestion_path,
        max_verified_index=_load_cache_max_n(path),
        proof_relevance=entry.proof_relevance,
        notes=entry.notes,
    )


if __name__ == "__main__":
    main()
