from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockedModeResult:
    mode: str
    implemented: bool
    reason: str
    gate_reached: str = "gate2_stub"
