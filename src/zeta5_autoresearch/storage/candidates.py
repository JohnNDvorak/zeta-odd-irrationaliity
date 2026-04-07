from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..config import CANDIDATES_DIR
from ..gate0_parse import parse_candidate_file
from ..models import Construction


def load_candidate(path: str | Path) -> Construction:
    return parse_candidate_file(path)


def candidate_snapshot_path(candidate: Construction, root: Path | None = CANDIDATES_DIR) -> Path:
    if not candidate.routing_hash:
        raise ValueError("candidate snapshot requires a routing_hash")
    snapshot_root = CANDIDATES_DIR if root is None else Path(root)
    return snapshot_root / f"{candidate.routing_hash}.json"


def save_candidate_snapshot(
    candidate: Construction,
    *,
    root: Path | None = CANDIDATES_DIR,
    extra_payload: dict[str, Any] | None = None,
) -> Path:
    path = candidate_snapshot_path(candidate, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _build_snapshot_payload(candidate, extra_payload=extra_payload)
    if path.exists():
        existing = load_candidate_snapshot(path)
        payload = _merge_snapshot_payloads(existing=existing, current=payload)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_candidate_snapshot(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _build_snapshot_payload(candidate: Construction, extra_payload: dict[str, Any] | None) -> dict[str, Any]:
    payload = candidate.to_display_dict()
    payload["snapshot_aliases"] = [candidate.id] if candidate.id else []
    payload["snapshot_variants"] = [_variant_record(candidate, extra_payload=extra_payload)]
    if extra_payload:
        payload.update(extra_payload)
    return payload


def _merge_snapshot_payloads(*, existing: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    canonical = _select_canonical_snapshot(existing=existing, current=current)
    aliases = _dedupe_strings([*existing.get("snapshot_aliases", []), existing.get("id"), *current.get("snapshot_aliases", []), current.get("id")])

    merged_variants = list(existing.get("snapshot_variants", []))
    if not merged_variants:
        merged_variants.append(_variant_record_from_snapshot(existing))
    current_variant = current.get("snapshot_variants", [])
    if current_variant:
        merged_variants.extend(current_variant)
    else:
        merged_variants.append(_variant_record_from_snapshot(current))
    merged_variants = _dedupe_variant_records(merged_variants)

    merged = _overlay_snapshot_metadata(dict(canonical), existing=existing, current=current)
    merged["snapshot_aliases"] = aliases
    merged["snapshot_variants"] = merged_variants
    return merged


def _select_canonical_snapshot(*, existing: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    existing_type = existing.get("mutation_type")
    current_type = current.get("mutation_type")
    if existing_type == "seed":
        return dict(existing)
    if current_type == "seed":
        return dict(current)
    return dict(existing)


def _variant_record(candidate: Construction, extra_payload: dict[str, Any] | None) -> dict[str, Any]:
    record = {
        "id": candidate.id,
        "mutation_type": candidate.mutation_type,
        "sequence_evidence_id": candidate.sequence_evidence_id,
        "sequence_hash": candidate.sequence_hash,
        "certificate_hash": candidate.certificate_hash,
        "representation": candidate.representation.presentation,
        "representation_detail": candidate.representation.detail,
        "equality_witness": candidate.representation.equality_witness,
        "certificate_template": candidate.certificate.template,
        "nu_p_method": candidate.certificate.nu_p_method,
        "hypothesis": candidate.hypothesis,
    }
    if extra_payload:
        record["extra"] = extra_payload
    return record


def _variant_record_from_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "mutation_type": payload.get("mutation_type"),
        "sequence_evidence_id": payload.get("sequence_evidence_id"),
        "sequence_hash": payload.get("sequence_hash"),
        "certificate_hash": payload.get("certificate_hash"),
        "representation": payload.get("representation", {}).get("presentation"),
        "representation_detail": payload.get("representation", {}).get("detail"),
        "equality_witness": payload.get("representation", {}).get("equality_witness"),
        "certificate_template": payload.get("certificate", {}).get("template"),
        "nu_p_method": payload.get("certificate", {}).get("nu_p_method"),
        "hypothesis": payload.get("hypothesis"),
    }


def _overlay_snapshot_metadata(canonical: dict[str, Any], *, existing: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    merged = dict(canonical)
    for key in ("sequence_evidence_id", "sequence_hash", "certificate_hash", "sequence_evidence", "gate1"):
        if _is_empty_snapshot_value(merged.get(key)):
            if not _is_empty_snapshot_value(current.get(key)):
                merged[key] = current[key]
            elif not _is_empty_snapshot_value(existing.get(key)):
                merged[key] = existing[key]
    return merged


def _is_empty_snapshot_value(value: Any) -> bool:
    return value in (None, "", [], {})


def _dedupe_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if not value:
            continue
        text = str(value)
        if text in seen:
            continue
        seen.add(text)
        deduped.append(text)
    return deduped


def _dedupe_variant_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for record in records:
        key = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)
    return deduped
