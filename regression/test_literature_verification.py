from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.literature_verification import (
    build_phase2_literature_claims,
    render_phase2_literature_verification_report,
    write_phase2_literature_verification_report,
)


def test_literature_verification_claims_cover_baseline_gap() -> None:
    claims = build_phase2_literature_claims()

    assert any(claim.verdict == "confirmed" and "equation (4)" in claim.location for claim in claims)
    assert any(claim.verdict == "confirmed" and "Section 2" in claim.location for claim in claims)
    assert any(
        claim.verdict == "not found" and "a=(8,16,10,15,12,16,18,13)" in claim.note
        for claim in claims
    )
    assert any(
        claim.verdict == "confirmed" and "third-order recurrence" in claim.note
        for claim in claims
    )
    assert any(
        claim.verdict == "confirmed" and "F_{5,1}" in claim.note
        for claim in claims
    )
    assert any(
        claim.verdict == "not found" and "Tosi" in claim.source
        for claim in claims
    )
    assert any(
        claim.verdict == "confirmed" and "A_σ8" in claim.note
        for claim in claims
    )
    assert any(
        claim.verdict == "confirmed" and "Dupont" in claim.source
        for claim in claims
    )
    assert any(
        claim.verdict == "confirmed" and "reflection-arrangement" in claim.note
        for claim in claims
    )
    assert any(
        claim.verdict == "confirmed" and "Some hypergeometric integrals" in claim.source
        for claim in claims
    )


def test_literature_verification_report_renders_and_writes(tmp_path: Path) -> None:
    report = render_phase2_literature_verification_report()

    assert "Phase 2 literature verification report" in report
    assert "arXiv:2210.03391v3" in report
    assert "not publish an explicit baseline non-symmetric `P_n` sequence" in report
    assert "Zudilin's 2002 `ζ(5)` recursion paper" in report
    assert "odd-zeta linear-form paper" in report
    assert "Tosi's 2026 explicit cellular-integral paper" in report
    assert "McCarthy-Osburn-Straub" in report
    assert "Dupont's odd-zeta motive paper" in report
    assert "Tosi's dissertation" in report
    assert "Zudilin's 2018 hypergeometric-integrals note" in report

    output = write_phase2_literature_verification_report(tmp_path / "lit.md")
    assert output.exists()
    assert "dual-linear-form concept" in output.read_text(encoding="utf-8")
