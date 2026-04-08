from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_experiment import DUAL_PROJECTION_PLAN_REPORT_PATH
from .dual_projection_target_spec import DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH
from .literature_verification import (
    LITERATURE_VERIFICATION_REPORT_PATH,
    build_phase2_literature_claims,
)

EXTERNAL_CALIBRATION_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_external_calibration_check.md"
EXTERNAL_CALIBRATION_JSON_PATH = CACHE_DIR / "bz_phase2_external_calibration_check.json"


@dataclass(frozen=True)
class CalibrationInvariant:
    invariant_id: str
    statement: str
    why_it_matters: str


@dataclass(frozen=True)
class ExternalCalibrationCheck:
    check_id: str
    chosen_anchor_id: str
    chosen_source: str
    chosen_location: str
    chosen_reason: str
    rejected_alternatives: tuple[str, ...]
    calibration_invariants: tuple[CalibrationInvariant, ...]
    success_condition: str
    next_probe_contract: str


def build_phase2_external_calibration_check() -> ExternalCalibrationCheck:
    claims = build_phase2_literature_claims()
    chosen_claim = next(
        claim
        for claim in claims
        if claim.source == "Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)"
        and claim.verdict == "confirmed"
    )

    return ExternalCalibrationCheck(
        check_id="bz_phase2_external_calibration_check",
        chosen_anchor_id="zudilin_2002_third_order_zeta5_bridge",
        chosen_source=chosen_claim.source,
        chosen_location=chosen_claim.location,
        chosen_reason=(
            "This is the strongest checked external bridge object because it publishes an explicit zeta(5) linear form "
            "q_n ζ(5) - p_n together with a companion zeta(3) channel. That makes it the closest verified analog to "
            "the baseline dual coefficient packet without pretending that the Brown-Zudilin baseline seed itself is explicit."
        ),
        rejected_alternatives=(
            "Zudilin 2002 odd-zeta paper: explicit but more generic; weaker as a convention lock than a single stated recurrence object.",
            "Zudilin 2018 hypergeometric-integrals note: explicit building blocks, but less direct as a first calibration target than q_n ζ(5) - p_n.",
            "McCarthy-Osburn-Straub 2020: denominator-side cellular data only; not a decay-side coefficient anchor.",
        ),
        calibration_invariants=(
            CalibrationInvariant(
                invariant_id="linear_form_normalization",
                statement=(
                    "The calibration anchor must be treated as an explicit linear form with a separated zeta(5) coefficient "
                    "and rational term, not as a black-box numeric remainder."
                ),
                why_it_matters=(
                    "The first baseline projection probe should preserve coefficient-level bookkeeping and must not collapse "
                    "its target into an opaque scalar too early."
                ),
            ),
            CalibrationInvariant(
                invariant_id="parasitic_channel_explicitness",
                statement=(
                    "A companion non-zeta(5) channel, here the zeta(3) side, should remain explicit instead of being hidden "
                    "inside a single projected object."
                ),
                why_it_matters=(
                    "The baseline dual target also carries companion channels, so the probe needs conventions that record "
                    "those channels honestly before any projection claim."
                ),
            ),
            CalibrationInvariant(
                invariant_id="sequence_level_reproducibility",
                statement=(
                    "The calibration anchor must be tied to published sequence-level data or recurrence data that another "
                    "implementer could reproduce."
                ),
                why_it_matters=(
                    "The baseline projection program should only promote objects whose conventions can be checked against an "
                    "explicit reference, not just against our own internal extraction choices."
                ),
            ),
        ),
        success_condition=(
            "The next baseline projection probe adopts these three invariants explicitly and names where its target object "
            "matches or departs from the external calibration anchor."
        ),
        next_probe_contract=(
            "The first bounded baseline projection probe must consume the baseline dual F_7 exact coefficient packet, state "
            "its coefficient-level normalization explicitly, preserve companion channels as named components, and report any "
            "asymmetry in component coverage before making a projection claim."
        ),
    )


def render_phase2_external_calibration_check() -> str:
    check = build_phase2_external_calibration_check()
    lines = [
        "# Phase 2 external calibration check",
        "",
        f"- Check id: `{check.check_id}`",
        f"- Chosen anchor id: `{check.chosen_anchor_id}`",
        f"- Chosen source: `{check.chosen_source}`",
        f"- Chosen location: `{check.chosen_location}`",
        f"- Literature verification report: `{LITERATURE_VERIFICATION_REPORT_PATH}`",
        f"- Dual projection plan: `{DUAL_PROJECTION_PLAN_REPORT_PATH}`",
        f"- Dual projection target spec: `{DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH}`",
        "",
        "## Why this anchor",
        "",
        check.chosen_reason,
        "",
        "## Rejected alternatives",
        "",
    ]
    for item in check.rejected_alternatives:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Calibration invariants",
            "",
        ]
    )
    for invariant in check.calibration_invariants:
        lines.extend(
            [
                f"### {invariant.invariant_id}",
                "",
                f"- Statement: {invariant.statement}",
                f"- Why it matters: {invariant.why_it_matters}",
                "",
            ]
        )
    lines.extend(
        [
            "## Success condition",
            "",
            check.success_condition,
            "",
            "## Next probe contract",
            "",
            check.next_probe_contract,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_external_calibration_check_report(
    output_path: str | Path = EXTERNAL_CALIBRATION_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_calibration_check(), encoding="utf-8")
    return output


def write_phase2_external_calibration_check_json(
    output_path: str | Path = EXTERNAL_CALIBRATION_JSON_PATH,
) -> Path:
    check = build_phase2_external_calibration_check()
    payload = {
        "check_id": check.check_id,
        "chosen_anchor_id": check.chosen_anchor_id,
        "chosen_source": check.chosen_source,
        "chosen_location": check.chosen_location,
        "chosen_reason": check.chosen_reason,
        "rejected_alternatives": list(check.rejected_alternatives),
        "calibration_invariants": [asdict(item) for item in check.calibration_invariants],
        "success_condition": check.success_condition,
        "next_probe_contract": check.next_probe_contract,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_calibration_check_report()
    write_phase2_external_calibration_check_json()


if __name__ == "__main__":
    main()
