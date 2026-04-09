from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .baseline_odd_pair_object_spec import (
    BASELINE_ODD_PAIR_OBJECT_SPEC_REPORT_PATH,
    build_baseline_odd_pair_object_spec,
)
from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string

BASELINE_ODD_EXTRACTION_RULE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_odd_extraction_rule.md"
)
BASELINE_ODD_EXTRACTION_RULE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_odd_extraction_rule.json"
)


@dataclass(frozen=True)
class BaselineOddExtractionRuleSample:
    n: int
    retained_zeta5: str
    retained_zeta3: str
    unresolved_constant: str


@dataclass(frozen=True)
class BaselineOddExtractionRule:
    rule_id: str
    source_spec_id: str
    shared_window_start: int
    shared_window_end: int
    rule_label: str
    rule_statement: str
    retained_output_hash: str
    unresolved_residual_hash: str
    extraction_summary_hash: str
    confirmed_output: tuple[str, ...]
    inferred_structure: tuple[str, ...]
    unresolved_structure: tuple[str, ...]
    bridge_boundary: str
    recommendation: str
    samples: tuple[BaselineOddExtractionRuleSample, ...]


def build_baseline_odd_extraction_rule() -> BaselineOddExtractionRule:
    spec = build_baseline_odd_pair_object_spec()

    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(spec.components[0].max_verified_index))
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(spec.components[1].max_verified_index, component="zeta3")
    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(spec.components[2].max_verified_index, component="constant")

    shared_window_end = min(len(zeta5_terms), len(zeta3_terms), len(constant_terms))
    retained_payload = [
        {
            "n": n,
            "zeta5": fraction_to_canonical_string(zeta5_term),
            "zeta3": fraction_to_canonical_string(zeta3_term),
        }
        for n, (zeta5_term, zeta3_term) in enumerate(
            zip(zeta5_terms[:shared_window_end], zeta3_terms[:shared_window_end]),
            start=1,
        )
    ]
    residual_payload = [
        {
            "n": n,
            "constant": fraction_to_canonical_string(constant_term),
        }
        for n, constant_term in enumerate(constant_terms[:shared_window_end], start=1)
    ]

    retained_output_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "baseline_odd_extraction_retained_output",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "terms": retained_payload,
        }
    )
    unresolved_residual_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "baseline_odd_extraction_unresolved_residual",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "terms": residual_payload,
        }
    )
    extraction_summary_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "baseline_odd_extraction_summary",
            "source_spec_id": spec.spec_id,
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "retained_output_hash": retained_output_hash,
            "unresolved_residual_hash": unresolved_residual_hash,
        }
    )

    samples = tuple(
        BaselineOddExtractionRuleSample(
            n=n,
            retained_zeta5=item["zeta5"],
            retained_zeta3=item["zeta3"],
            unresolved_constant=residual_payload[n - 1]["constant"],
        )
        for n, item in enumerate(retained_payload[:3], start=1)
    )

    return BaselineOddExtractionRule(
        rule_id="bz_phase2_baseline_odd_extraction_rule_v1",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=shared_window_end,
        rule_label="Retain `(zeta(5), zeta(3))` as the active odd-weight extraction pair and carry the constant term as unresolved residual",
        rule_statement=(
            "The bounded odd-pair extraction rule promotes the baseline-side pair `(zeta(5), zeta(3))` to the active extraction output "
            "object and carries the rational constant term explicitly as unresolved residual structure. No baseline remainder or "
            "bridge-fit identity is asserted."
        ),
        retained_output_hash=retained_output_hash,
        unresolved_residual_hash=unresolved_residual_hash,
        extraction_summary_hash=extraction_summary_hash,
        confirmed_output=(
            "The retained odd-weight extraction output is an exact repo-native ordered pair over the shared window.",
            "The unresolved constant residual remains exact and explicit over the same shared window.",
            "The full odd-pair extraction summary is reproducible via retained and residual hashes.",
        ),
        inferred_structure=(
            "This rule treats the odd-weight pair as the next baseline-native extraction object after the `(constant, zeta(5))` line hit a hard wall.",
            "This rule interprets the constant term as residual structure rather than part of the active odd pair.",
        ),
        unresolved_structure=(
            "No baseline P_n sequence has been extracted.",
            "No baseline remainder pipeline has been proved.",
            "No rule eliminating the constant residual is claimed.",
        ),
        bridge_boundary=spec.bridge_boundary,
        recommendation=(
            "Run one bounded odd-pair extraction probe next and require its report to preserve the split between retained odd channels and unresolved constant residual."
        ),
        samples=samples,
    )


def render_baseline_odd_extraction_rule() -> str:
    rule = build_baseline_odd_extraction_rule()
    lines = [
        "# Phase 2 baseline odd extraction rule",
        "",
        f"- Rule id: `{rule.rule_id}`",
        f"- Source spec: `{BASELINE_ODD_PAIR_OBJECT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{rule.source_spec_id}`",
        f"- Shared exact window: `n={rule.shared_window_start}..{rule.shared_window_end}`",
        f"- Rule label: {rule.rule_label}",
        f"- Retained output hash: `{rule.retained_output_hash}`",
        f"- Unresolved residual hash: `{rule.unresolved_residual_hash}`",
        f"- Extraction summary hash: `{rule.extraction_summary_hash}`",
        "",
        "## Rule statement",
        "",
        rule.rule_statement,
        "",
        "## Confirmed output",
        "",
    ]
    for item in rule.confirmed_output:
        lines.append(f"- {item}")
    lines.extend(["", "## Inferred structure", ""])
    for item in rule.inferred_structure:
        lines.append(f"- {item}")
    lines.extend(["", "## Unresolved structure", ""])
    for item in rule.unresolved_structure:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Bridge boundary",
            "",
            rule.bridge_boundary,
            "",
            "## Sample retained / residual data",
            "",
            "| n | retained zeta(5) | retained zeta(3) | unresolved constant |",
            "| --- | --- | --- | --- |",
        ]
    )
    for sample in rule.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.retained_zeta5}` | `{sample.retained_zeta3}` | `{sample.unresolved_constant}` |"
        )
    lines.extend(["", "## Recommendation", "", rule.recommendation, ""])
    return "\n".join(lines)


def write_baseline_odd_extraction_rule_report(
    output_path: str | Path = BASELINE_ODD_EXTRACTION_RULE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_odd_extraction_rule(), encoding="utf-8")
    return output


def write_baseline_odd_extraction_rule_json(
    output_path: str | Path = BASELINE_ODD_EXTRACTION_RULE_JSON_PATH,
) -> Path:
    rule = build_baseline_odd_extraction_rule()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(rule), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_odd_extraction_rule_report()
    write_baseline_odd_extraction_rule_json()


if __name__ == "__main__":
    main()
