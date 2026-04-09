from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_odd_extraction_rule import (
    BASELINE_ODD_EXTRACTION_RULE_REPORT_PATH,
    build_baseline_odd_extraction_rule,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_ODD_EXTRACTION_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_odd_extraction_probe.md"
)
BASELINE_ODD_EXTRACTION_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_odd_extraction_probe.json"
)


@dataclass(frozen=True)
class BaselineOddExtractionProbeSample:
    n: int
    retained_zeta5: str
    retained_zeta3: str
    unresolved_constant: str


@dataclass(frozen=True)
class BaselineOddExtractionProbe:
    probe_id: str
    source_rule_id: str
    shared_window_start: int
    shared_window_end: int
    retained_output_hash: str
    unresolved_residual_hash: str
    extraction_summary_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    bridge_boundary: str
    recommendation: str
    samples: tuple[BaselineOddExtractionProbeSample, ...]


def build_baseline_odd_extraction_probe() -> BaselineOddExtractionProbe:
    rule = build_baseline_odd_extraction_rule()
    samples = tuple(
        BaselineOddExtractionProbeSample(
            n=sample.n,
            retained_zeta5=sample.retained_zeta5,
            retained_zeta3=sample.retained_zeta3,
            unresolved_constant=sample.unresolved_constant,
        )
        for sample in rule.samples
    )

    return BaselineOddExtractionProbe(
        probe_id="bz_phase2_baseline_odd_extraction_probe_v1",
        source_rule_id=rule.rule_id,
        shared_window_start=rule.shared_window_start,
        shared_window_end=rule.shared_window_end,
        retained_output_hash=rule.retained_output_hash,
        unresolved_residual_hash=rule.unresolved_residual_hash,
        extraction_summary_hash=rule.extraction_summary_hash,
        verdict="baseline_odd_pair_summary_established",
        stabilized_findings=(
            "A baseline odd-pair extraction summary now exists on the exact shared window `n=1..80`.",
            "The retained odd-weight output and the unresolved constant residual are independently reproducible via exact hashes.",
            "The active extraction object is defined directly on baseline-side data and keeps the odd-zeta channels together.",
        ),
        unresolved_findings=(
            "No baseline `P_n` sequence has been extracted.",
            "No baseline remainder pipeline has been proved.",
            "The constant residual remains unresolved rather than eliminated.",
        ),
        bridge_boundary=rule.bridge_boundary,
        recommendation=(
            "Add the odd-pair post-probe decision gate next. It should decide whether this odd-weight baseline summary is strong enough "
            "to justify one bounded residual-refinement ladder."
        ),
        samples=samples,
    )


def render_baseline_odd_extraction_probe() -> str:
    probe = build_baseline_odd_extraction_probe()
    lines = [
        "# Phase 2 baseline odd extraction probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source rule: `{BASELINE_ODD_EXTRACTION_RULE_REPORT_PATH}`",
        f"- Source rule id: `{probe.source_rule_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Retained output hash: `{probe.retained_output_hash}`",
        f"- Unresolved residual hash: `{probe.unresolved_residual_hash}`",
        f"- Extraction summary hash: `{probe.extraction_summary_hash}`",
        f"- Verdict: `{probe.verdict}`",
        "",
        "## Stabilized findings",
        "",
    ]
    for item in probe.stabilized_findings:
        lines.append(f"- {item}")
    lines.extend(["", "## Unresolved findings", ""])
    for item in probe.unresolved_findings:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Bridge boundary",
            "",
            probe.bridge_boundary,
            "",
            "## Sample retained / residual data",
            "",
            "| n | retained zeta(5) | retained zeta(3) | unresolved constant |",
            "| --- | --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.retained_zeta5}` | `{sample.retained_zeta3}` | `{sample.unresolved_constant}` |"
        )
    lines.extend(["", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_baseline_odd_extraction_probe_report(
    output_path: str | Path = BASELINE_ODD_EXTRACTION_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_odd_extraction_probe(), encoding="utf-8")
    return output


def write_baseline_odd_extraction_probe_json(
    output_path: str | Path = BASELINE_ODD_EXTRACTION_PROBE_JSON_PATH,
) -> Path:
    probe = build_baseline_odd_extraction_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_odd_extraction_probe_report()
    write_baseline_odd_extraction_probe_json()


if __name__ == "__main__":
    main()
