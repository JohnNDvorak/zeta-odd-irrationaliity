from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .bz_symmetric_linear_forms_probe import _lcm_upto, _load_linear_forms_fixture, _load_shared_recurrence
from .gate2.recurrence_eval import generate_terms_from_recurrence
from .gate2.sequence_identity import MinimalRecurrenceIdentity


@dataclass(frozen=True)
class SymmetricLinearFormsExactPacket:
    packet_id: str
    fixture_id: str
    recurrence_evidence_id: str
    source_title: str
    source_url: str
    source_version: str
    q_scale_label: str
    p_scale_label: str
    phat_scale_label: str
    shared_window_start: int
    shared_window_end: int
    scaled_q_terms: tuple[Fraction, ...]
    scaled_p_terms: tuple[Fraction, ...]
    scaled_phat_terms: tuple[Fraction, ...]


def build_symmetric_linear_forms_exact_packet(*, max_n: int = 80) -> SymmetricLinearFormsExactPacket:
    if max_n < 5:
        raise ValueError("max_n must be at least 5")

    fixture = _load_linear_forms_fixture()
    q_recurrence = _load_shared_recurrence(fixture.q_recurrence_evidence_id)
    p_recurrence = MinimalRecurrenceIdentity(
        start_index=q_recurrence.start_index,
        initial_values=fixture.p_initial,
        terms=q_recurrence.terms,
    )
    phat_recurrence = MinimalRecurrenceIdentity(
        start_index=q_recurrence.start_index,
        initial_values=fixture.phat_initial,
        terms=q_recurrence.terms,
    )

    q_terms = generate_terms_from_recurrence(q_recurrence, max_index=max_n)
    p_terms = generate_terms_from_recurrence(p_recurrence, max_index=max_n)
    phat_terms = generate_terms_from_recurrence(phat_recurrence, max_index=max_n)

    scaled_q_terms = []
    scaled_p_terms = []
    scaled_phat_terms = []
    for n in range(1, max_n + 1):
        d_n = _lcm_upto(n)
        d_2n = _lcm_upto(2 * n)
        scaled_q_terms.append(q_terms[n] * (d_n**5))
        scaled_p_terms.append(p_terms[n] * (d_n**5))
        scaled_phat_terms.append(phat_terms[n] * (d_n**2) * d_2n)

    return SymmetricLinearFormsExactPacket(
        packet_id="bz_totally_symmetric_scaled_linear_forms_packet",
        fixture_id=fixture.id,
        recurrence_evidence_id=fixture.q_recurrence_evidence_id,
        source_title=fixture.source_title,
        source_url=fixture.source_url,
        source_version=fixture.source_version,
        q_scale_label=fixture.q_scale_label,
        p_scale_label=fixture.p_scale_label,
        phat_scale_label=fixture.phat_scale_label,
        shared_window_start=1,
        shared_window_end=max_n,
        scaled_q_terms=tuple(scaled_q_terms),
        scaled_p_terms=tuple(scaled_p_terms),
        scaled_phat_terms=tuple(scaled_phat_terms),
    )
