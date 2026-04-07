from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Gate3BlockedResult:
    implemented: bool
    reason: str
    gate_reached: str = "gate3_stub"


def run_gate3() -> Gate3BlockedResult:
    return Gate3BlockedResult(
        implemented=False,
        reason="Gate 3 certification is deferred until the denominator theorems and CAS bridge are wired in.",
    )
