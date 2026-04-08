from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .construction_memo import CONSTRUCTION_MEMO_REPORT_PATH
from .dual_f7_exact_coefficient_cache import (
    BASELINE_DUAL_F7_CONSTANT_CACHE_PATH,
    BASELINE_DUAL_F7_ZETA3_CACHE_PATH,
)
from .dual_f7_zeta5_cache import BASELINE_DUAL_F7_ZETA5_CACHE_PATH
from .dual_projection_experiment import (
    DUAL_PROJECTION_PLAN_REPORT_PATH,
    build_phase2_dual_projection_experiment_plan,
)
from .literature_verification import LITERATURE_VERIFICATION_REPORT_PATH

DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_dual_projection_target_spec.md"
DUAL_PROJECTION_TARGET_SPEC_JSON_PATH = CACHE_DIR / "bz_phase2_dual_projection_target_spec.json"


@dataclass(frozen=True)
class ProjectionComponentSpec:
    component_id: str
    role: str
    cache_path: str
    max_verified_index: int
    exact_status: str
    note: str


@dataclass(frozen=True)
class DualProjectionTargetSpec:
    target_id: str
    target_label: str
    baseline_seed: str
    target_kind: str
    projection_meaning: str
    non_claims: tuple[str, ...]
    source_basis: tuple[str, ...]
    components: tuple[ProjectionComponentSpec, ...]
    recommended_use: str


def build_phase2_dual_projection_target_spec() -> DualProjectionTargetSpec:
    plan = build_phase2_dual_projection_experiment_plan()
    return DualProjectionTargetSpec(
        target_id="baseline_dual_f7_exact_coefficient_packet",
        target_label="Baseline dual F_7 exact coefficient packet",
        baseline_seed=plan.baseline_seed,
        target_kind="pre_projection_exact_coefficient_packet",
        projection_meaning=(
            "This target is the exact displayed-series coefficient packet of the Brown-Zudilin baseline dual F_7 "
            "linear form: rational constant term, zeta(3) coefficient, and zeta(5) coefficient. It is the smallest "
            "repo-native object that already exists exactly and can honestly feed a later parity/projection step "
            "without pretending that a baseline P_n sequence has been extracted."
        ),
        non_claims=(
            "This target is not a published baseline P_n sequence.",
            "This target is not a proved baseline remainder pipeline.",
            "This target does not by itself isolate the Brown-Zudilin baseline decay object.",
        ),
        source_basis=(
            f"Construction memo: {CONSTRUCTION_MEMO_REPORT_PATH}",
            f"Dual projection experiment plan: {DUAL_PROJECTION_PLAN_REPORT_PATH}",
            f"Literature verification report: {LITERATURE_VERIFICATION_REPORT_PATH}",
        ),
        components=(
            ProjectionComponentSpec(
                component_id="constant",
                role="rational constant term of the exact dual F_7 linear form",
                cache_path=str(BASELINE_DUAL_F7_CONSTANT_CACHE_PATH),
                max_verified_index=_load_cache_max_n(BASELINE_DUAL_F7_CONSTANT_CACHE_PATH),
                exact_status="exact",
                note=(
                    "Extracted by the exact dual F_7 linear-form path and cached as canonical rationals. "
                    "This is the strongest exact baseline companion lane currently banked."
                ),
            ),
            ProjectionComponentSpec(
                component_id="zeta3",
                role="exact zeta(3) coefficient of the dual F_7 linear form",
                cache_path=str(BASELINE_DUAL_F7_ZETA3_CACHE_PATH),
                max_verified_index=_load_cache_max_n(BASELINE_DUAL_F7_ZETA3_CACHE_PATH),
                exact_status="exact",
                note=(
                    "Extracted alongside the constant term from the exact dual F_7 linear-form path and "
                    "cached as canonical rationals."
                ),
            ),
            ProjectionComponentSpec(
                component_id="zeta5",
                role="exact zeta(5) coefficient of the dual F_7 linear form",
                cache_path=str(BASELINE_DUAL_F7_ZETA5_CACHE_PATH),
                max_verified_index=_load_cache_max_n(BASELINE_DUAL_F7_ZETA5_CACHE_PATH),
                exact_status="exact",
                note=(
                    "Available from the faster zeta(5)-only exact extractor. Its verified frontier is shorter than "
                    "the constant/zeta(3) companion caches, so any first projection probe must state that asymmetry explicitly."
                ),
            ),
        ),
        recommended_use=(
            "Use this exact coefficient packet as the first bounded projection target. A projection experiment may "
            "recombine or filter these three exact components, but it must preserve the distinction between "
            "pre-projection coefficient data and any claimed baseline decay sequence."
        ),
    )


def render_phase2_dual_projection_target_spec() -> str:
    spec = build_phase2_dual_projection_target_spec()
    lines = [
        "# Phase 2 dual projection target spec",
        "",
        f"- Target id: `{spec.target_id}`",
        f"- Target label: `{spec.target_label}`",
        f"- Baseline seed: `{spec.baseline_seed}`",
        f"- Target kind: `{spec.target_kind}`",
        "",
        "## Projection meaning",
        "",
        spec.projection_meaning,
        "",
        "## Non-claims",
        "",
    ]
    for item in spec.non_claims:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Source basis",
            "",
        ]
    )
    for item in spec.source_basis:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Components",
            "",
            "| component | role | max verified index | exact status | cache path |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for component in spec.components:
        lines.append(
            f"| `{component.component_id}` | {component.role} | `{component.max_verified_index}` | "
            f"`{component.exact_status}` | `{component.cache_path}` |"
        )
    lines.extend(
        [
            "",
            "## Component notes",
            "",
        ]
    )
    for component in spec.components:
        lines.append(f"- `{component.component_id}`: {component.note}")
    lines.extend(
        [
            "",
            "## Recommended use",
            "",
            spec.recommended_use,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_dual_projection_target_spec_report(
    output_path: str | Path = DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_dual_projection_target_spec(), encoding="utf-8")
    return output


def write_phase2_dual_projection_target_spec_json(
    output_path: str | Path = DUAL_PROJECTION_TARGET_SPEC_JSON_PATH,
) -> Path:
    spec = build_phase2_dual_projection_target_spec()
    payload = {
        "target_id": spec.target_id,
        "target_label": spec.target_label,
        "baseline_seed": spec.baseline_seed,
        "target_kind": spec.target_kind,
        "projection_meaning": spec.projection_meaning,
        "non_claims": list(spec.non_claims),
        "source_basis": list(spec.source_basis),
        "components": [asdict(component) for component in spec.components],
        "recommended_use": spec.recommended_use,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def _load_cache_max_n(path: str | Path) -> int:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return int(payload["max_n"])


def main() -> None:
    write_phase2_dual_projection_target_spec_report()
    write_phase2_dual_projection_target_spec_json()


if __name__ == "__main__":
    main()
