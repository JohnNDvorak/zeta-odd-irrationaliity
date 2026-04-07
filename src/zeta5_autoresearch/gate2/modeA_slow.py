from __future__ import annotations

from .common import BlockedModeResult


def run_mode_a_slow() -> BlockedModeResult:
    return BlockedModeResult(
        mode="Mode A-slow",
        implemented=False,
        reason="Sequence identity and C2 evaluation remain blocked on CAS-backed Gate 2 work.",
    )
