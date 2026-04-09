from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .canonicalize import canonicalize_affine_family
from .hashes import compute_routing_hash
from .models import Construction, SpecValidationError, construction_from_dict


@dataclass(frozen=True)
class Gate0Result:
    candidate: Construction
    canonicalization_permutation: tuple[int, ...]
    canonicalized: bool


def parse_candidate_data(payload: dict[str, Any]) -> Construction:
    if "construction" not in payload:
        raise SpecValidationError("root mapping must contain 'construction'")
    construction_payload = payload["construction"]
    return construction_from_dict(construction_payload)


def parse_candidate_file(path: str | Path) -> Construction:
    raw = Path(path).read_text(encoding="utf-8")
    payload = yaml.safe_load(raw)
    if not isinstance(payload, dict):
        raise SpecValidationError("candidate file must contain a mapping at the root")
    return parse_candidate_data(payload)


def run_gate0(path: str | Path) -> Gate0Result:
    candidate = parse_candidate_file(path)
    canonical_affine, permutation = canonicalize_affine_family(candidate.affine_family)
    canonicalized = canonical_affine != candidate.affine_family
    candidate = candidate.with_affine_family(canonical_affine)
    routing_hash = compute_routing_hash(candidate.to_routing_payload())
    candidate = candidate.with_hashes(routing_hash=routing_hash)
    return Gate0Result(candidate=candidate, canonicalization_permutation=permutation, canonicalized=canonicalized)
