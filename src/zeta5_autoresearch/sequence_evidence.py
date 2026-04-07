from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .config import REPO_ROOT
from .gate2.sequence_identity import MinimalRecurrenceIdentity, RecurrenceTerm
from .hashes import compute_certificate_hash, compute_sequence_hash
from .models import Construction, SpecValidationError, fraction_from_scalar, fraction_to_canonical_string

SEQUENCE_EVIDENCE_DIR = REPO_ROOT / "specs" / "evidence"


@dataclass(frozen=True)
class SequenceEvidence:
    id: str
    sequence_hash_status: str
    evidence_kind: str
    scope: str
    normalization: str
    candidate_ids: tuple[str, ...]
    candidate_id_prefixes: tuple[str, ...]
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    locked_configuration_label: str
    locked_family_label: str
    locked_support_class: str
    locked_u: tuple[str, ...]
    locked_v: tuple[str, ...]
    locked_extraction_method: str
    locked_auxiliary_forms: int
    start_index: int
    order_bound: int | None
    initial_data: tuple[str, ...]
    signature: tuple[str, ...]
    recurrence: MinimalRecurrenceIdentity | None

    def applies_to_candidate(self, candidate: Construction) -> bool:
        if candidate.id is None:
            return False
        id_match = candidate.id in self.candidate_ids or any(candidate.id.startswith(prefix) for prefix in self.candidate_id_prefixes)
        if not id_match:
            return False
        return self.matches_locked_candidate(candidate)

    def matches_locked_candidate(self, candidate: Construction) -> bool:
        if candidate.configuration.label != self.locked_configuration_label:
            return False
        if candidate.configuration.family_label != self.locked_family_label:
            return False
        if candidate.configuration.support_class != self.locked_support_class:
            return False
        if candidate.affine_family.to_hashable_payload()["u"] != list(self.locked_u):
            return False
        if candidate.affine_family.to_hashable_payload()["v"] != list(self.locked_v):
            return False
        if candidate.extraction.method != self.locked_extraction_method:
            return False
        if candidate.extraction.auxiliary_forms != self.locked_auxiliary_forms:
            return False
        return True

    def compute_hash(self) -> str:
        if self.evidence_kind == "minimal_recurrence":
            if self.recurrence is None:
                raise SpecValidationError("minimal_recurrence evidence requires recurrence data")
            return compute_sequence_hash(
                minimal_annihilator={
                    "evidence_id": self.id,
                    "status": self.sequence_hash_status,
                    "scope": self.scope,
                    "normalization": self.normalization,
                    "recurrence": self.recurrence.to_hash_payload(),
                }
            )
        if self.evidence_kind != "provisional_q_sequence_signature":
            raise SpecValidationError(f"unsupported evidence kind {self.evidence_kind!r}")
        return compute_sequence_hash(
            provisional_signature={
                "evidence_id": self.id,
                "status": self.sequence_hash_status,
                "scope": self.scope,
                "normalization": self.normalization,
                "start_index": self.start_index,
                "order_bound": self.order_bound,
                "initial_data": list(self.initial_data),
                "signature": list(self.signature),
            }
        )

    def to_metadata(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "sequence_hash_status": self.sequence_hash_status,
            "evidence_kind": self.evidence_kind,
            "scope": self.scope,
            "normalization": self.normalization,
            "locked_candidate": {
                "configuration_label": self.locked_configuration_label,
                "family_label": self.locked_family_label,
                "support_class": self.locked_support_class,
                "u": list(self.locked_u),
                "v": list(self.locked_v),
                "extraction_method": self.locked_extraction_method,
                "auxiliary_forms": self.locked_auxiliary_forms,
            },
            "source": {
                "title": self.source_title,
                "url": self.source_url,
                "version": self.source_version,
                "notes": self.source_notes,
            },
        }


def resolve_candidate_sequence_evidence(candidate: Construction) -> tuple[Construction, SequenceEvidence | None]:
    if not candidate.sequence_evidence_id:
        return candidate, None
    evidence = load_sequence_evidence_by_id(candidate.sequence_evidence_id)
    if not evidence.applies_to_candidate(candidate):
        raise SpecValidationError(
            f"sequence evidence {evidence.id!r} does not apply to candidate {candidate.id!r}"
        )
    sequence_hash = evidence.compute_hash()
    certificate_hash = compute_certificate_hash(
        sequence_hash=sequence_hash,
        representation=candidate.representation.presentation,
        template=candidate.certificate.template,
        nu_p_method=candidate.certificate.nu_p_method,
    )
    return candidate.with_hashes(sequence_hash=sequence_hash, certificate_hash=certificate_hash), evidence


def load_sequence_evidence_by_id(evidence_id: str, root: Path = SEQUENCE_EVIDENCE_DIR) -> SequenceEvidence:
    for path in sorted(Path(root).glob("*.yaml")):
        evidence = load_sequence_evidence_file(path)
        if evidence.id == evidence_id:
            return evidence
    raise FileNotFoundError(f"no sequence evidence with id {evidence_id!r} found in {root}")


def load_sequence_evidence_file(path: str | Path) -> SequenceEvidence:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "sequence_evidence" not in payload:
        raise SpecValidationError("sequence evidence file must contain a root 'sequence_evidence' mapping")

    root = payload["sequence_evidence"]
    if not isinstance(root, dict):
        raise SpecValidationError("sequence_evidence must be a mapping")

    _require_keys(
        root,
        (
            "id",
            "sequence_hash_status",
            "evidence_kind",
            "scope",
            "normalization",
            "locked_candidate",
            "applies_to",
            "source",
        ),
        "sequence_evidence",
    )
    applies_to = _require_mapping(root["applies_to"], "sequence_evidence.applies_to")
    locked_candidate = _require_mapping(root["locked_candidate"], "sequence_evidence.locked_candidate")
    source = _require_mapping(root["source"], "sequence_evidence.source")

    evidence_kind = str(root["evidence_kind"])
    if evidence_kind == "minimal_recurrence":
        recurrence_payload = _require_mapping(root["recurrence"], "sequence_evidence.recurrence")
        terms_payload = recurrence_payload.get("terms")
        if not isinstance(terms_payload, list) or not terms_payload:
            raise SpecValidationError("minimal_recurrence evidence requires a non-empty recurrence.terms list")
        recurrence = MinimalRecurrenceIdentity.from_scalars(
            start_index=int(recurrence_payload["start_index"]),
            initial_values=recurrence_payload["initial_values"],
            terms=tuple(
                RecurrenceTerm.from_scalars(
                    shift=int(term["shift"]),
                    coefficients=term["coefficients"],
                )
                for term in terms_payload
            ),
        )
        start_index = recurrence.start_index
        order_bound = len(recurrence.terms) - 1
        initial_data = tuple(fraction_to_canonical_string(value) for value in recurrence.initial_values)
        signature = ()
    else:
        provisional = _require_mapping(root["provisional_signature"], "sequence_evidence.provisional_signature")
        start_index = int(provisional["start_index"])
        order_bound = int(provisional["order_bound"])
        initial_data = tuple(
            fraction_to_canonical_string(fraction_from_scalar(value))
            for value in provisional["initial_data"]
        )
        signature = tuple(
            fraction_to_canonical_string(fraction_from_scalar(value))
            for value in provisional["signature"]
        )
        recurrence = None

    return SequenceEvidence(
        id=str(root["id"]),
        sequence_hash_status=str(root["sequence_hash_status"]),
        evidence_kind=evidence_kind,
        scope=str(root["scope"]),
        normalization=str(root["normalization"]),
        candidate_ids=tuple(str(value) for value in applies_to.get("candidate_ids", [])),
        candidate_id_prefixes=tuple(str(value) for value in applies_to.get("candidate_id_prefixes", [])),
        source_title=str(source["title"]),
        source_url=str(source["url"]),
        source_version=str(source.get("version", "")),
        source_notes=str(source.get("notes", "")),
        locked_configuration_label=str(locked_candidate["configuration_label"]),
        locked_family_label=str(locked_candidate["family_label"]),
        locked_support_class=str(locked_candidate["support_class"]),
        locked_u=tuple(str(value) for value in locked_candidate["affine_family"]["u"]),
        locked_v=tuple(str(value) for value in locked_candidate["affine_family"]["v"]),
        locked_extraction_method=str(locked_candidate["extraction"]["method"]),
        locked_auxiliary_forms=int(locked_candidate["extraction"]["auxiliary_forms"]),
        start_index=start_index,
        order_bound=order_bound,
        initial_data=initial_data,
        signature=signature,
        recurrence=recurrence,
    )


def _require_mapping(payload: Any, name: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SpecValidationError(f"{name} must be a mapping")
    return payload


def _require_keys(payload: dict[str, Any], keys: tuple[str, ...], name: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise SpecValidationError(f"{name} missing required keys: {', '.join(missing)}")
