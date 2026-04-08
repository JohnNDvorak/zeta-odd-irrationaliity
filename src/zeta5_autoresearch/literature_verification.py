from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import DATA_DIR

LITERATURE_VERIFICATION_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_literature_verification_report.md"


@dataclass(frozen=True)
class LiteratureClaim:
    claim: str
    applies_to: str
    source: str
    location: str
    verdict: str
    note: str


def build_phase2_literature_claims() -> tuple[LiteratureClaim, ...]:
    return (
        LiteratureClaim(
            claim="The general 8-parameter family is decomposed into Q, P, and P-hat coefficients.",
            applies_to="general family",
            source="Brown-Zudilin, arXiv:2210.03391v3",
            location="Introduction, equation (4)",
            verdict="confirmed",
            note=(
                "The paper explicitly writes I = Q·(2ζ(5)+4ζ(3)ζ(2)) - 4 P̂·ζ(2) - 2 P, "
                "with Q, P, P̂ in Q and Q in Z."
            ),
        ),
        LiteratureClaim(
            claim="The totally symmetric specialization has explicit initial values for Q_n, P_n, and P-hat_n and a third-order recurrence.",
            applies_to="totally symmetric specialization",
            source="Brown-Zudilin, arXiv:2210.03391v3",
            location="Section 2, equation (5) and the recurrence immediately after it",
            verdict="confirmed",
            note=(
                "Section 2 gives Q_0,Q_1,Q_2, P_0,P_1,P_2, P̂_0,P̂_1,P̂_2 and states that the same third-order "
                "Apéry-type recursion is satisfied by I_n, Q_n, P_n, and P̂_n."
            ),
        ),
        LiteratureClaim(
            claim="The baseline non-symmetric seed a=(8,16,10,15,12,16,18,13) has an explicit published P_n sequence or baseline recurrence.",
            applies_to="baseline specialization",
            source="Brown-Zudilin, arXiv:2210.03391v3",
            location="Section 11",
            verdict="not found",
            note=(
                "Section 11 gives the concrete matrix, asymptotics for I(a n), I'(a n)=Q_n ζ(5)-P_n, "
                "and the worthiness calculation, but in the checked text it does not give explicit baseline initial values "
                "for P_n, nor an explicit baseline recurrence analogous to Section 2."
            ),
        ),
        LiteratureClaim(
            claim="Dual cellular forms can be projected to linear forms in 1 and ζ(5).",
            applies_to="dual family / conceptual precursor",
            source="Brown, Irrationality proofs, moduli spaces and dinner parties (2014 notes)",
            location="Section 7.1 and Appendix 2 table discussion",
            verdict="confirmed",
            note=(
                "The notes state that dual generalized cellular integrals can be projected by setting ζ^m(2)=0, "
                "yielding linear forms in 1 and ζ(2m-3), and for 8π8∨ mention extraction of linear forms in 1 and ζ(5)."
            ),
        ),
        LiteratureClaim(
            claim="Brown's 2014 notes publish an explicit baseline-seed P_n sequence for the later Brown-Zudilin non-symmetric seed.",
            applies_to="baseline specialization",
            source="Brown, Irrationality proofs, moduli spaces and dinner parties (2014 notes)",
            location="Section 7.1 and Appendix 2",
            verdict="not found",
            note=(
                "The notes provide conceptual and experimental dual-linear-form examples, but the checked text does not identify "
                "the later baseline seed a=(8,16,10,15,12,16,18,13) or publish an explicit baseline P_n sequence for it."
            ),
        ),
        LiteratureClaim(
            claim="There exists an explicit independent recurrence-based linear-form construction q_n ζ(5)-p_n in the older literature.",
            applies_to="independent ζ(5) bridge object",
            source="Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)",
            location="Theorem 1, equations (1) and (2)",
            verdict="confirmed",
            note=(
                "This paper gives a third-order recurrence together with explicit initial data for q_n, p_n, and p̃_n, "
                "producing ℓ_n = q_n ζ(5) - p_n and a companion ℓ̃_n = q_n ζ(3) - p̃_n. It is a real decay-side bridge, "
                "but it is not the Brown-Zudilin baseline cellular family."
            ),
        ),
        LiteratureClaim(
            claim="The 2025 Cohen-Zudilin Apéry-variations paper gives a direct Brown-Zudilin baseline decay extraction.",
            applies_to="baseline specialization",
            source="Cohen-Zudilin, Variations on a theme of Apéry (2025)",
            location="Abstract and scanned scope",
            verdict="not found",
            note=(
                "The checked text is about continued-fraction variations and explicitly says no new irrationality results are given. "
                "Nothing checked so far ties it directly to the Brown-Zudilin baseline cellular seed."
            ),
        ),
        LiteratureClaim(
            claim="Zudilin's 2002 arithmetic-of-linear-forms paper gives generic hypergeometric ζ(5)-side bridge objects.",
            applies_to="independent ζ(5) bridge framework",
            source="Zudilin, Arithmetic of linear forms involving odd zeta values (2002)",
            location="Section 8 and formulas around J_n(5), F_{5,1}",
            verdict="confirmed",
            note=(
                "The paper gives well-poised hypergeometric constructions whose specialization produces linear forms involving "
                "ζ(5), ζ(3), and 1, for example D_n^5·J_n(5) in Zζ(5)+Zζ(3)+Z and F_{5,1}=18ζ(5)+66ζ(3)-98. "
                "This is a real external bridge framework, but not a Brown-Zudilin baseline cellular extraction."
            ),
        ),
        LiteratureClaim(
            claim="Zudilin's 2003 'Well-poised hypergeometric service' paper gives a direct Brown-Zudilin baseline decay extraction.",
            applies_to="baseline specialization",
            source="Zudilin, Well-poised hypergeometric service for diophantine problems of zeta values (2003)",
            location="checked scope",
            verdict="not found",
            note=(
                "The checked arXiv version appears to concern a ζ(4) recursion line rather than the Brown-Zudilin cellular "
                "baseline or an explicit non-symmetric ζ(5) decay extraction."
            ),
        ),
        LiteratureClaim(
            claim="Tosi's 2026 explicit cellular-integral paper gives a direct extraction for the Brown-Zudilin generalized 8-parameter baseline family.",
            applies_to="baseline specialization",
            source="Tosi, An explicit study of a family of cellular integrals (2026)",
            location="Abstract and scanned introduction",
            verdict="not found",
            note=(
                "The paper explicitly studies a simpler family of basic cellular integrals and cites Brown-Zudilin as motivation, "
                "but in the checked text it does not address the generalized non-symmetric 8-parameter Brown-Zudilin baseline seed."
            ),
        ),
        LiteratureClaim(
            claim="The modular-forms paper on sequences associated to Brown's cellular integrals gives explicit denominator-side sequence data for an N=8 family.",
            applies_to="basic cellular bridge framework",
            source="McCarthy-Osburn-Straub, Sequences, modular forms and cellular integrals (2020)",
            location="Section 3.1, Proposition 3.1 and Remark 3.2",
            verdict="confirmed",
            note=(
                "For the basic self-dual configuration σ8=(8,3,6,1,4,7,2,5), the paper studies the leading coefficient A_σ8(n), "
                "gives explicit initial terms, a binomial-sum representation, and reports a fourth-order recurrence. "
                "This is useful denominator-side cellular data, but not the Brown-Zudilin generalized baseline decay sequence."
            ),
        ),
        LiteratureClaim(
            claim="Dupont's odd-zeta motive paper gives a general integral formula for coefficients and a geometric explanation of parity vanishing in odd-zeta linear forms.",
            applies_to="general odd-zeta coefficient framework",
            source="Dupont, Odd zeta motive and linear forms in odd zeta values (2018)",
            location="Theorems 1.1 and 1.2; Theorem 1.3 / 1.4 overview in the introduction",
            verdict="confirmed",
            note=(
                "Dupont gives general cycle-integral formulas for the coefficients a_k(ω) of linear forms in zeta values and "
                "a geometric explanation of even/odd coefficient vanishing via the involution τ. This is conceptually close to "
                "the projection/parity issues in the Brown-Zudilin program, but it does not directly give the non-symmetric baseline "
                "P_n sequence for a=(8,16,10,15,12,16,18,13)."
            ),
        ),
        LiteratureClaim(
            claim="Tosi's dissertation gives a broader geometric framework that traces some later irrationality linear forms to generalized cellular-type periods.",
            applies_to="broader geometric bridge framework",
            source="Tosi, dissertation / reflection-arrangement framework (2026)",
            location="Introduction and Theorem 2 discussion",
            verdict="confirmed",
            note=(
                "The dissertation states that its reflection-arrangement period framework generalizes Brown's approach and can attach a geometric origin "
                "to some later irrationality linear forms such as those in Zudilin 2019. This is a genuine broadening of the geometric picture, "
                "but it still does not provide a direct explicit extraction of the Brown-Zudilin non-symmetric baseline decay sequence."
            ),
        ),
        LiteratureClaim(
            claim="Zudilin's 2018 hypergeometric-integrals note gives general integral representations for odd-zeta linear-form building blocks.",
            applies_to="independent odd-zeta bridge framework",
            source="Zudilin, Some hypergeometric integrals for linear forms in zeta values (2018)",
            location="Theorem 1 and introduction",
            verdict="confirmed",
            note=(
                "The note gives integral representations for general linear-form building blocks in Hurwitz zeta and odd zeta values, with arithmetic control on coefficients. "
                "It is another explicit bridge framework, but not a Brown-Zudilin cellular-baseline extraction."
            ),
        ),
    )


def render_phase2_literature_verification_report() -> str:
    claims = build_phase2_literature_claims()
    lines = [
        "# Phase 2 literature verification report",
        "",
        "This report records only claims checked directly against primary sources already inspected in this research cycle.",
        "It does not claim an exhaustive literature closure beyond those sources.",
        "",
        "## Executive result",
        "",
        "- The current Brown-Zudilin paper, `arXiv:2210.03391v3` dated January 29, 2026, explicitly treats the totally symmetric case at the sequence level.",
        "- In the checked text, the same paper does not publish an explicit baseline non-symmetric `P_n` sequence or baseline recurrence for `a=(8,16,10,15,12,16,18,13)`.",
        "- Brown's earlier 2014 notes support the dual-linear-form concept but do not close that baseline-seed gap.",
        "- Zudilin's 2002 `ζ(5)` recursion paper gives a genuine external decay-side bridge object, but it is not the Brown-Zudilin baseline cellular sequence.",
        "- Zudilin's broader 2002 odd-zeta linear-form paper also gives a generic hypergeometric `ζ(5)` bridge framework, again external to the Brown-Zudilin baseline seed.",
        "- Tosi's 2026 explicit cellular-integral paper appears relevant at the general cellular-integral level, but not as a direct extraction for the Brown-Zudilin generalized baseline family.",
        "- McCarthy-Osburn-Straub's modular-forms paper gives explicit denominator-side data for a basic `N=8` cellular family, but still not the generalized Brown-Zudilin baseline decay object.",
        "- Dupont's odd-zeta motive paper gives the cleanest verified conceptual bridge so far for coefficient formulas and parity vanishing, but still not a direct baseline-seed extraction.",
        "- Tosi's dissertation broadens the geometric framework beyond moduli-space cellular integrals, but still does not directly extract the Brown-Zudilin baseline decay side.",
        "- Zudilin's 2018 hypergeometric-integrals note adds another explicit odd-zeta bridge framework, but still not the Brown-Zudilin baseline sequence.",
        "",
        "| claim | applies to | source | location | verdict |",
        "| --- | --- | --- | --- | --- |",
    ]
    for claim in claims:
        lines.append(
            f"| {claim.claim} | `{claim.applies_to}` | `{claim.source}` | `{claim.location}` | `{claim.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
        ]
    )
    for claim in claims:
        lines.append(f"- `{claim.verdict}`: {claim.note}")
    lines.extend(
        [
            "",
            "## Next search step",
            "",
            "- Search adjacent primary sources for any later explicit extraction of the baseline non-symmetric decay side, not just the symmetric anchor or the conceptual dual family.",
            "- Treat Zudilin's 2002 recurrence construction as the strongest checked external bridge object for comparison, not as evidence that the Brown-Zudilin baseline seed itself is explicit.",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_literature_verification_report(
    output_path: str | Path = LITERATURE_VERIFICATION_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_literature_verification_report(), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_literature_verification_report()


if __name__ == "__main__":
    main()
