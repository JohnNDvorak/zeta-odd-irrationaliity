from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .config import REPO_ROOT
from .gate0_parse import run_gate0
from .gate1_filter import run_gate1
from .models import Certificate, Construction, Representation, SpecValidationError
from .sequence_evidence import resolve_candidate_sequence_evidence

CAMPAIGN_MODE_CHOICES = frozenset({"Mode A-fast", "Mode A-slow", "Mode B"})
EQUALITY_PRESERVATION_CHOICES = frozenset({"witnessed", "claimed_unverified"})


@dataclass(frozen=True)
class CampaignVariantSpec:
    id_suffix: str
    mode: str
    equality_preservation: str
    representation: Representation
    certificate: Certificate
    notes: str


@dataclass(frozen=True)
class CampaignSpec:
    id: str
    label: str
    family: str
    base_candidate: Path
    locked: tuple[str, ...]
    mutation_from: str | None
    target_improvement: str
    variants: tuple[CampaignVariantSpec, ...]


@dataclass(frozen=True)
class ExpandedCampaignCandidate:
    variant: CampaignVariantSpec
    candidate: Construction
    gate1_accepted: bool
    gate1_errors: tuple[str, ...]
    gate1_warnings: tuple[str, ...]


def load_campaign_spec(path: str | Path) -> CampaignSpec:
    raw_path = Path(path)
    payload = yaml.safe_load(raw_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "campaign" not in payload or not isinstance(payload["campaign"], dict):
        raise SpecValidationError("campaign file must contain a root 'campaign' mapping")

    campaign = payload["campaign"]
    _require_keys(campaign, ("id", "label", "family", "base_candidate", "locked", "defaults", "variants"), "campaign")
    defaults = campaign["defaults"]
    if not isinstance(defaults, dict):
        raise SpecValidationError("campaign.defaults must be a mapping")

    variants_payload = campaign["variants"]
    if not isinstance(variants_payload, list) or not variants_payload:
        raise SpecValidationError("campaign.variants must be a non-empty list")

    base_candidate = (REPO_ROOT / str(campaign["base_candidate"])).resolve()
    variants = tuple(_parse_variant(item) for item in variants_payload)

    return CampaignSpec(
        id=str(campaign["id"]),
        label=str(campaign["label"]),
        family=str(campaign["family"]),
        base_candidate=base_candidate,
        locked=tuple(str(value) for value in campaign["locked"]),
        mutation_from=None if defaults.get("mutation_from") is None else str(defaults["mutation_from"]),
        target_improvement=str(defaults.get("target_improvement", campaign["family"])),
        variants=variants,
    )


def expand_campaign(path: str | Path) -> tuple[CampaignSpec, tuple[ExpandedCampaignCandidate, ...]]:
    campaign = load_campaign_spec(path)
    base_gate0 = run_gate0(campaign.base_candidate)
    base_candidate = base_gate0.candidate

    expanded: list[ExpandedCampaignCandidate] = []
    for variant in campaign.variants:
        candidate = Construction(
            id=_candidate_id(base_candidate.id, variant.id_suffix),
            routing_hash=None,
            sequence_hash=base_candidate.sequence_hash,
            certificate_hash=None,
            sequence_evidence_id=base_candidate.sequence_evidence_id,
            configuration=base_candidate.configuration,
            affine_family=base_candidate.affine_family,
            extraction=base_candidate.extraction,
            representation=variant.representation,
            certificate=variant.certificate,
            motive=base_candidate.motive,
            hypothesis=f"Fixed-sequence campaign variant: {variant.id_suffix}. {variant.notes}",
            target_improvement=campaign.target_improvement,
            mutation_from=campaign.mutation_from,
            mutation_type="campaign_variant",
        )
        candidate_path = write_candidate_variant(candidate, campaign_id=campaign.id)
        gate0 = run_gate0(candidate_path)
        resolved_candidate, _ = resolve_candidate_sequence_evidence(gate0.candidate)
        gate1 = run_gate1(gate0)
        expanded.append(
            ExpandedCampaignCandidate(
                variant=variant,
                candidate=resolved_candidate,
                gate1_accepted=gate1.accepted,
                gate1_errors=gate1.errors,
                gate1_warnings=gate1.warnings,
            )
        )

    return campaign, tuple(expanded)


def write_candidate_variant(candidate: Construction, *, campaign_id: str) -> Path:
    output_dir = REPO_ROOT / "specs" / "generated" / campaign_id
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{candidate.id}.yaml"
    payload = {"construction": candidate.to_display_dict()}
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
    return path


def run_campaign_structural_dry_run(path: str | Path, *, log_results: bool = False) -> dict[str, Any]:
    campaign, expanded = expand_campaign(path)
    rows: list[dict[str, Any]] = []
    for item in expanded:
        row: dict[str, Any] = {
            "variant_id": item.candidate.id,
            "mode": item.variant.mode,
            "representation": item.candidate.representation.presentation,
            "certificate_template": item.candidate.certificate.template,
            "routing_hash": item.candidate.routing_hash,
            "sequence_hash": item.candidate.sequence_hash,
            "certificate_hash": item.candidate.certificate_hash,
            "gate1_accepted": item.gate1_accepted,
            "gate1_errors": list(item.gate1_errors),
            "gate1_warnings": list(item.gate1_warnings),
            "notes": item.variant.notes,
        }
        if log_results:
            from .orchestrator import log_structural_run

            generated_path = REPO_ROOT / "specs" / "generated" / campaign.id / f"{item.candidate.id}.yaml"
            row["logging"] = log_structural_run(
                candidate_path=generated_path,
                mode=item.variant.mode,
                notes=f"campaign={campaign.id}; {item.variant.notes}",
            )
        rows.append(row)

    return {
        "campaign_id": campaign.id,
        "label": campaign.label,
        "variants": rows,
    }


def _parse_variant(payload: Any) -> CampaignVariantSpec:
    if not isinstance(payload, dict):
        raise SpecValidationError("campaign variant must be a mapping")
    _require_keys(payload, ("id_suffix", "mode", "equality_preservation", "representation", "certificate", "notes"), "campaign variant")

    mode = str(payload["mode"])
    if mode not in CAMPAIGN_MODE_CHOICES:
        raise SpecValidationError(f"unsupported campaign mode {mode!r}")

    equality_preservation = str(payload["equality_preservation"])
    if equality_preservation not in EQUALITY_PRESERVATION_CHOICES:
        raise SpecValidationError(f"unsupported equality_preservation {equality_preservation!r}")

    representation_payload = payload["representation"]
    certificate_payload = payload["certificate"]
    if not isinstance(representation_payload, dict) or not isinstance(certificate_payload, dict):
        raise SpecValidationError("campaign variant representation and certificate must be mappings")

    representation = Representation(
        presentation=str(representation_payload["presentation"]),
        detail=str(representation_payload["detail"]),
        equality_witness=str(representation_payload["equality_witness"]),
    )
    certificate = Certificate(
        template=str(certificate_payload["template"]),
        nu_p_method=str(certificate_payload["nu_p_method"]),
        human_review_needed=bool(certificate_payload["human_review_needed"]),
    )

    if mode == "Mode A-fast" and representation.equality_witness in {"", "none"}:
        raise SpecValidationError("Mode A-fast campaign variants require a non-empty equality witness")
    if mode == "Mode A-slow" and equality_preservation != "claimed_unverified":
        raise SpecValidationError("Mode A-slow variants must be marked claimed_unverified")

    return CampaignVariantSpec(
        id_suffix=str(payload["id_suffix"]),
        mode=mode,
        equality_preservation=equality_preservation,
        representation=representation,
        certificate=certificate,
        notes=str(payload["notes"]),
    )


def _candidate_id(base_id: str | None, suffix: str) -> str:
    stem = base_id or "campaign_candidate"
    return f"{stem}__{suffix}"


def _require_keys(payload: dict[str, Any], keys: tuple[str, ...], name: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise SpecValidationError(f"{name} missing required keys: {', '.join(missing)}")
