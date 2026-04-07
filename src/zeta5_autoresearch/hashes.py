from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


class SequenceHashUnavailable(RuntimeError):
    """Raised when a semantic sequence hash is requested before implementation exists."""


class CertificateHashUnavailable(RuntimeError):
    """Raised when a certificate hash is requested before a sequence hash exists."""


def _stable_hash(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def compute_routing_hash(payload: Mapping[str, Any]) -> str:
    return _stable_hash(payload)


def compute_sequence_hash(*, minimal_annihilator: Any | None = None, provisional_signature: Any | None = None) -> str:
    if minimal_annihilator is None and provisional_signature is None:
        raise SequenceHashUnavailable("sequence_hash is deferred until Gate 2 / CAS integration exists")
    if minimal_annihilator is not None:
        return _stable_hash({"kind": "minimal_annihilator", "payload": minimal_annihilator})
    return _stable_hash({"kind": "provisional_sequence_signature", "payload": provisional_signature})


def compute_certificate_hash(
    *,
    sequence_hash: str | None,
    representation: str,
    template: str,
    nu_p_method: str,
    certificate_parameters: Mapping[str, Any] | None = None,
) -> str:
    if not sequence_hash:
        raise CertificateHashUnavailable("certificate_hash requires a verified sequence_hash")
    payload = {
        "sequence_hash": sequence_hash,
        "representation": representation,
        "template": template,
        "nu_p_method": nu_p_method,
        "certificate_parameters": dict(certificate_parameters or {}),
    }
    return _stable_hash(payload)
