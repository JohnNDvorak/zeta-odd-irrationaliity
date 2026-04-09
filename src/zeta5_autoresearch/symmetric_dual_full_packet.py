from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .dual_f7_exact_coefficient_cache import get_cached_symmetric_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_symmetric_dual_f7_zeta5_terms


@dataclass(frozen=True)
class SymmetricDualFullPacket:
    packet_id: str
    shared_window_start: int
    shared_window_end: int
    constant_terms: tuple[Fraction, ...]
    zeta3_terms: tuple[Fraction, ...]
    zeta5_terms: tuple[Fraction, ...]


def build_symmetric_dual_full_packet(*, max_n: int = 80) -> SymmetricDualFullPacket:
    if max_n <= 0:
        raise ValueError("max_n must be positive")

    constant_terms = get_cached_symmetric_dual_f7_exact_component_terms(max_n, component="constant")
    zeta3_terms = get_cached_symmetric_dual_f7_exact_component_terms(max_n, component="zeta3")
    zeta5_terms = tuple(Fraction(value) for value in get_cached_symmetric_dual_f7_zeta5_terms(max_n))
    return SymmetricDualFullPacket(
        packet_id="bz_phase2_symmetric_dual_full_packet",
        shared_window_start=1,
        shared_window_end=max_n,
        constant_terms=constant_terms,
        zeta3_terms=zeta3_terms,
        zeta5_terms=zeta5_terms,
    )
