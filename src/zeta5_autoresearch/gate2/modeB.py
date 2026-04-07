from __future__ import annotations

from .common import BlockedModeResult


def run_mode_b() -> BlockedModeResult:
    return BlockedModeResult(
        mode="Mode B",
        implemented=False,
        reason="Full sequence search is intentionally blocked until Gate 2 and Gate 3 are implemented.",
    )
