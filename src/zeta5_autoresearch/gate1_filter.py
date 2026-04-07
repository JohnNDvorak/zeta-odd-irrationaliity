from __future__ import annotations

from dataclasses import dataclass

from .config import KNOWN_CONFIGURATION_SUPPORT, KNOWN_EXCLUDED_ROUTING_HASHES, SUPPORTED_CERTIFICATE_TEMPLATES
from .gate0_parse import Gate0Result
from .lattice import ConvergenceCheckResult, ParityCheckResult, check_all_n_parity, check_convergence


@dataclass(frozen=True)
class Gate1Result:
    accepted: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    parity: ParityCheckResult
    convergence: ConvergenceCheckResult


def run_gate1(gate0: Gate0Result) -> Gate1Result:
    candidate = gate0.candidate
    errors: list[str] = []
    warnings: list[str] = []

    parity = check_all_n_parity(candidate.affine_family)
    if not parity.valid:
        errors.extend(parity.failures)

    convergence = check_convergence(candidate.affine_family)
    if not convergence.valid:
        errors.extend(convergence.failures)

    if candidate.routing_hash in KNOWN_EXCLUDED_ROUTING_HASHES:
        errors.append("candidate routing_hash is on the known exclusion list")

    expected = KNOWN_CONFIGURATION_SUPPORT.get(candidate.configuration.label)
    if expected is None:
        warnings.append(f"unknown configuration label {candidate.configuration.label!r}; support screen left conservative")
    else:
        if candidate.configuration.family_label != expected["family_label"]:
            errors.append(
                "configuration family_label mismatch: "
                f"expected {expected['family_label']!r}, got {candidate.configuration.family_label!r}"
            )
        if candidate.configuration.support_class != expected["support_class"]:
            errors.append(
                "configuration support_class mismatch: "
                f"expected {expected['support_class']!r}, got {candidate.configuration.support_class!r}"
            )

    if candidate.certificate.template not in SUPPORTED_CERTIFICATE_TEMPLATES:
        errors.append(f"unsupported certificate template {candidate.certificate.template!r}")

    return Gate1Result(
        accepted=not errors,
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
        parity=parity,
        convergence=convergence,
    )
