from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import sys
from typing import Any, Mapping


class SpecValidationError(ValueError):
    """Raised when a candidate spec does not satisfy the structural schema."""


def fraction_from_scalar(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, bool):
        raise SpecValidationError("boolean values are not valid rational scalars")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(str(value))
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise SpecValidationError("empty string is not a valid rational scalar")
        try:
            return _fraction_from_decimal_string(text)
        except ValueError as exc:
            raise SpecValidationError(f"invalid rational scalar: {value!r}") from exc
    raise SpecValidationError(f"unsupported rational scalar type: {type(value).__name__}")


def fraction_to_canonical_string(value: Fraction) -> str:
    if value.denominator == 1:
        return _int_to_decimal_string(value.numerator)
    return f"{_int_to_decimal_string(value.numerator)}/{_int_to_decimal_string(value.denominator)}"


def serialize_fraction_sequence(values: tuple[Fraction, ...]) -> list[str]:
    return [fraction_to_canonical_string(value) for value in values]


def _int_to_decimal_string(value: int) -> str:
    if not hasattr(sys, "get_int_max_str_digits"):
        return str(value)

    current_limit = sys.get_int_max_str_digits()
    if current_limit == 0:
        return str(value)

    sys.set_int_max_str_digits(0)
    try:
        return str(value)
    finally:
        sys.set_int_max_str_digits(current_limit)


def _fraction_from_decimal_string(text: str) -> Fraction:
    if not hasattr(sys, "get_int_max_str_digits"):
        return Fraction(text)

    current_limit = sys.get_int_max_str_digits()
    if current_limit == 0:
        return Fraction(text)

    sys.set_int_max_str_digits(0)
    try:
        return Fraction(text)
    finally:
        sys.set_int_max_str_digits(current_limit)


def _require_mapping(payload: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise SpecValidationError(f"{name} must be a mapping")
    return payload


def _require_keys(payload: Mapping[str, Any], *, name: str, keys: tuple[str, ...]) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        missing_text = ", ".join(missing)
        raise SpecValidationError(f"{name} is missing required keys: {missing_text}")


def _normalize_fraction_vector(values: Any, *, name: str) -> tuple[Fraction, ...]:
    if not isinstance(values, list):
        raise SpecValidationError(f"{name} must be a list")
    if len(values) != 8:
        raise SpecValidationError(f"{name} must contain exactly 8 entries")
    return tuple(fraction_from_scalar(value) for value in values)


@dataclass(frozen=True)
class Configuration:
    label: str
    family_label: str
    support_class: str


@dataclass(frozen=True)
class AffineFamily:
    u: tuple[Fraction, ...]
    v: tuple[Fraction, ...]

    def to_hashable_payload(self) -> dict[str, list[str]]:
        return {
            "u": serialize_fraction_sequence(self.u),
            "v": serialize_fraction_sequence(self.v),
        }


@dataclass(frozen=True)
class Extraction:
    method: str
    auxiliary_forms: int
    description: str


@dataclass(frozen=True)
class Representation:
    presentation: str
    detail: str
    equality_witness: str


@dataclass(frozen=True)
class Certificate:
    template: str
    nu_p_method: str
    human_review_needed: bool


@dataclass(frozen=True)
class Motive:
    observed_signature: str | None
    proved_signature: str | None
    observed_rank: int | None
    proved_rank: int | None


@dataclass(frozen=True)
class Construction:
    id: str | None
    routing_hash: str | None
    sequence_hash: str | None
    certificate_hash: str | None
    sequence_evidence_id: str | None
    configuration: Configuration
    affine_family: AffineFamily
    extraction: Extraction
    representation: Representation
    certificate: Certificate
    motive: Motive
    hypothesis: str
    target_improvement: str
    mutation_from: str | None
    mutation_type: str

    def with_affine_family(self, affine_family: AffineFamily) -> "Construction":
        return Construction(
            id=self.id,
            routing_hash=self.routing_hash,
            sequence_hash=self.sequence_hash,
            certificate_hash=self.certificate_hash,
            sequence_evidence_id=self.sequence_evidence_id,
            configuration=self.configuration,
            affine_family=affine_family,
            extraction=self.extraction,
            representation=self.representation,
            certificate=self.certificate,
            motive=self.motive,
            hypothesis=self.hypothesis,
            target_improvement=self.target_improvement,
            mutation_from=self.mutation_from,
            mutation_type=self.mutation_type,
        )

    def with_hashes(
        self,
        *,
        routing_hash: str | None = None,
        sequence_hash: str | None = None,
        certificate_hash: str | None = None,
    ) -> "Construction":
        return Construction(
            id=self.id,
            routing_hash=self.routing_hash if routing_hash is None else routing_hash,
            sequence_hash=self.sequence_hash if sequence_hash is None else sequence_hash,
            certificate_hash=self.certificate_hash if certificate_hash is None else certificate_hash,
            sequence_evidence_id=self.sequence_evidence_id,
            configuration=self.configuration,
            affine_family=self.affine_family,
            extraction=self.extraction,
            representation=self.representation,
            certificate=self.certificate,
            motive=self.motive,
            hypothesis=self.hypothesis,
            target_improvement=self.target_improvement,
            mutation_from=self.mutation_from,
            mutation_type=self.mutation_type,
        )

    def to_routing_payload(self) -> dict[str, Any]:
        return {
            "configuration_label": self.configuration.label,
            "affine_family": self.affine_family.to_hashable_payload(),
            "extraction_method": self.extraction.method,
            "representation": self.representation.presentation,
            "certificate_template": self.certificate.template,
            "nu_p_method": self.certificate.nu_p_method,
        }

    def to_display_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "routing_hash": self.routing_hash,
            "sequence_hash": self.sequence_hash,
            "certificate_hash": self.certificate_hash,
            "sequence_evidence_id": self.sequence_evidence_id,
            "configuration": {
                "label": self.configuration.label,
                "family_label": self.configuration.family_label,
                "support_class": self.configuration.support_class,
            },
            "affine_family": self.affine_family.to_hashable_payload(),
            "extraction": {
                "method": self.extraction.method,
                "auxiliary_forms": self.extraction.auxiliary_forms,
                "description": self.extraction.description,
            },
            "representation": {
                "presentation": self.representation.presentation,
                "detail": self.representation.detail,
                "equality_witness": self.representation.equality_witness,
            },
            "certificate": {
                "template": self.certificate.template,
                "nu_p_method": self.certificate.nu_p_method,
                "human_review_needed": self.certificate.human_review_needed,
            },
            "motive": {
                "observed_signature": self.motive.observed_signature,
                "proved_signature": self.motive.proved_signature,
                "observed_rank": self.motive.observed_rank,
                "proved_rank": self.motive.proved_rank,
            },
            "hypothesis": self.hypothesis,
            "target_improvement": self.target_improvement,
            "mutation_from": self.mutation_from,
            "mutation_type": self.mutation_type,
        }


def construction_from_dict(payload: Mapping[str, Any]) -> Construction:
    _require_keys(payload, name="construction", keys=("configuration", "affine_family", "extraction", "representation", "certificate", "motive"))

    configuration = _require_mapping(payload["configuration"], "construction.configuration")
    _require_keys(configuration, name="construction.configuration", keys=("label", "family_label", "support_class"))

    affine_family = _require_mapping(payload["affine_family"], "construction.affine_family")
    _require_keys(affine_family, name="construction.affine_family", keys=("u", "v"))

    extraction = _require_mapping(payload["extraction"], "construction.extraction")
    _require_keys(extraction, name="construction.extraction", keys=("method", "auxiliary_forms", "description"))

    representation = _require_mapping(payload["representation"], "construction.representation")
    _require_keys(representation, name="construction.representation", keys=("presentation", "detail", "equality_witness"))

    certificate = _require_mapping(payload["certificate"], "construction.certificate")
    _require_keys(certificate, name="construction.certificate", keys=("template", "nu_p_method", "human_review_needed"))

    motive = _require_mapping(payload["motive"], "construction.motive")
    _require_keys(motive, name="construction.motive", keys=("observed_signature", "proved_signature", "observed_rank", "proved_rank"))

    return Construction(
        id=payload.get("id"),
        routing_hash=payload.get("routing_hash"),
        sequence_hash=payload.get("sequence_hash"),
        certificate_hash=payload.get("certificate_hash"),
        sequence_evidence_id=None if payload.get("sequence_evidence_id") is None else str(payload["sequence_evidence_id"]),
        configuration=Configuration(
            label=str(configuration["label"]),
            family_label=str(configuration["family_label"]),
            support_class=str(configuration["support_class"]),
        ),
        affine_family=AffineFamily(
            u=_normalize_fraction_vector(affine_family["u"], name="construction.affine_family.u"),
            v=_normalize_fraction_vector(affine_family["v"], name="construction.affine_family.v"),
        ),
        extraction=Extraction(
            method=str(extraction["method"]),
            auxiliary_forms=int(extraction["auxiliary_forms"]),
            description=str(extraction["description"]),
        ),
        representation=Representation(
            presentation=str(representation["presentation"]),
            detail=str(representation["detail"]),
            equality_witness=str(representation["equality_witness"]),
        ),
        certificate=Certificate(
            template=str(certificate["template"]),
            nu_p_method=str(certificate["nu_p_method"]),
            human_review_needed=bool(certificate["human_review_needed"]),
        ),
        motive=Motive(
            observed_signature=None if motive["observed_signature"] is None else str(motive["observed_signature"]),
            proved_signature=None if motive["proved_signature"] is None else str(motive["proved_signature"]),
            observed_rank=None if motive["observed_rank"] is None else int(motive["observed_rank"]),
            proved_rank=None if motive["proved_rank"] is None else int(motive["proved_rank"]),
        ),
        hypothesis=str(payload.get("hypothesis", "")),
        target_improvement=str(payload.get("target_improvement", "")),
        mutation_from=None if payload.get("mutation_from") is None else str(payload["mutation_from"]),
        mutation_type=str(payload.get("mutation_type", "")),
    )
