from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .config import DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_projection_probe import (
    DUAL_PROJECTION_PROBE_REPORT_PATH,
    build_phase2_dual_projection_probe,
)
from .external_calibration_check import EXTERNAL_CALIBRATION_REPORT_PATH
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string

DUAL_PROJECTION_RULE_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_dual_projection_rule_experiment.md"


@dataclass(frozen=True)
class ProjectionRuleSample:
    n: int
    retained_constant: str
    retained_zeta5: str
    residual_zeta3: str


@dataclass(frozen=True)
class DualProjectionRuleExperiment:
    experiment_id: str
    rule_id: str
    rule_label: str
    shared_window_start: int
    shared_window_end: int
    retained_pair_hash: str
    residual_channel_hash: str
    packet_source_hash: str
    rule_meaning: str
    non_claims: tuple[str, ...]
    matches_to_calibration: tuple[str, ...]
    departures_from_calibration: tuple[str, ...]
    samples: tuple[ProjectionRuleSample, ...]
    recommendation: str


def build_phase2_dual_projection_rule_experiment() -> DualProjectionRuleExperiment:
    probe = build_phase2_dual_projection_probe()

    shared_window_end = probe.shared_window_end
    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(shared_window_end, component="constant")
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(shared_window_end, component="zeta3")
    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(shared_window_end))

    retained_pair_payload = []
    residual_payload = []
    samples = []
    for n, (constant_term, zeta3_term, zeta5_term) in enumerate(zip(constant_terms, zeta3_terms, zeta5_terms), start=1):
        retained_pair_payload.append(
            {
                "n": n,
                "constant": fraction_to_canonical_string(constant_term),
                "zeta5": fraction_to_canonical_string(zeta5_term),
            }
        )
        residual_payload.append(
            {
                "n": n,
                "zeta3": fraction_to_canonical_string(zeta3_term),
            }
        )
        if n <= 3:
            samples.append(
                ProjectionRuleSample(
                    n=n,
                    retained_constant=fraction_to_canonical_string(constant_term),
                    retained_zeta5=fraction_to_canonical_string(zeta5_term),
                    residual_zeta3=fraction_to_canonical_string(zeta3_term),
                )
            )

    retained_pair_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "dual_projection_retained_pair",
            "rule_id": "keep_constant_and_zeta5_carry_zeta3_residual_v1",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "terms": retained_pair_payload,
        }
    )
    residual_channel_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "dual_projection_residual_channel",
            "rule_id": "keep_constant_and_zeta5_carry_zeta3_residual_v1",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "terms": residual_payload,
        }
    )

    return DualProjectionRuleExperiment(
        experiment_id="bz_phase2_dual_projection_rule_experiment_v1",
        rule_id="keep_constant_and_zeta5_carry_zeta3_residual_v1",
        rule_label="Keep `(constant, zeta(5))` as the retained pair and carry `zeta(3)` as an explicit residual channel",
        shared_window_start=1,
        shared_window_end=shared_window_end,
        retained_pair_hash=retained_pair_hash,
        residual_channel_hash=residual_channel_hash,
        packet_source_hash=probe.packet_hash,
        rule_meaning=(
            "This is a bookkeeping projection rule inspired by the odd-target isolation idea in the verified literature. "
            "It does not set the zeta(3) channel to zero or claim a motivic projection theorem. It only freezes the "
            "two-channel `(constant, zeta(5))` pair as the retained target while carrying the exact zeta(3) channel as "
            "an explicit residual companion on the same shared window."
        ),
        non_claims=(
            "This rule does not prove that the retained pair equals a baseline P_n or baseline remainder sequence.",
            "This rule does not justify dropping the zeta(3) channel analytically; it only records it separately as residual data.",
            "This rule does not claim any irrationality consequence by itself.",
        ),
        matches_to_calibration=(
            "The retained object is still a coefficient-level linear-form object rather than a black-box scalar.",
            "The companion zeta(3) channel remains explicit as residual data instead of being hidden.",
            "The retained pair and residual channel are both hashed on the same exact shared window, preserving reproducibility.",
        ),
        departures_from_calibration=(
            "The calibration anchor gives a published q_n ζ(5) - p_n linear form, while this rule only defines a retained pair and residual channel.",
            "The rule is bookkeeping-only: it does not derive a recurrence or prove that the residual channel can be eliminated.",
            "The retained pair still inherits the baseline packet's shorter shared window n<=80 because the zeta(5) cache is the limiting component.",
        ),
        samples=tuple(samples),
        recommendation=(
            "Use this retained-pair / residual-channel split as the baseline for the next decision gate. The next step should "
            "either propose one stronger projection identity to test against this split or stop and fall back to the external bridge path."
        ),
    )


def render_phase2_dual_projection_rule_experiment() -> str:
    experiment = build_phase2_dual_projection_rule_experiment()
    lines = [
        "# Phase 2 dual projection rule experiment",
        "",
        f"- Experiment id: `{experiment.experiment_id}`",
        f"- Rule id: `{experiment.rule_id}`",
        f"- Rule label: {experiment.rule_label}",
        f"- Source packet report: `{DUAL_PROJECTION_PROBE_REPORT_PATH}`",
        f"- Calibration report: `{EXTERNAL_CALIBRATION_REPORT_PATH}`",
        f"- Shared exact window: `n={experiment.shared_window_start}..{experiment.shared_window_end}`",
        f"- Source packet hash: `{experiment.packet_source_hash}`",
        f"- Retained pair hash: `{experiment.retained_pair_hash}`",
        f"- Residual channel hash: `{experiment.residual_channel_hash}`",
        "",
        "## Rule meaning",
        "",
        experiment.rule_meaning,
        "",
        "## Matches to calibration",
        "",
    ]
    for item in experiment.matches_to_calibration:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Departures from calibration",
            "",
        ]
    )
    for item in experiment.departures_from_calibration:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Non-claims",
            "",
        ]
    )
    for item in experiment.non_claims:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Sample retained / residual data",
            "",
            "| n | retained constant | retained zeta(5) | residual zeta(3) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for sample in experiment.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.retained_constant}` | `{sample.retained_zeta5}` | `{sample.residual_zeta3}` |"
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            experiment.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_dual_projection_rule_experiment_report(
    output_path: str | Path = DUAL_PROJECTION_RULE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_dual_projection_rule_experiment(), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_dual_projection_rule_experiment_report()


if __name__ == "__main__":
    main()
