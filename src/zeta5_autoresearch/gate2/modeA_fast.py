from __future__ import annotations

from .common import BlockedModeResult


def run_mode_a_fast() -> BlockedModeResult:
    return BlockedModeResult(
        mode="Mode A-fast",
        implemented=False,
        reason="Gate 2 scoring is deferred until a validated CAS backend is available.",
    )
