from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import yaml

from .config import REPO_ROOT

WIKI_DIRNAME = "wiki"
RAW_DIRNAME = "raw"

WIKI_CATEGORY_DIRS = {
    "entity": "entities",
    "concept": "concepts",
    "source": "sources",
    "audit": "audits",
    "frontier": "",
    "code": "code",
    "literature": "literature",
    "computation": "computation",
    "conclusion": "conclusions",
    "exploration": "explorations",
}

KEY_CODE_SNAPSHOTS = (
    "src/zeta5_autoresearch/bz_dual_f7.py",
    "src/zeta5_autoresearch/dual_f7_exact_coefficient_cache.py",
    "src/zeta5_autoresearch/bz_symmetric_linear_forms_probe.py",
    "src/zeta5_autoresearch/orchestrator.py",
    "src/zeta5_autoresearch/gate0_parse.py",
    "src/zeta5_autoresearch/gate1_filter.py",
    "src/zeta5_autoresearch/campaign_report.py",
    "src/zeta5_autoresearch/baseline_residual_refinement_decision_gate.py",
    "src/zeta5_autoresearch/symmetric_dual_baseline_chart_transfer_decision_gate.py",
)

DATE_FMT = "%Y-%m-%d"

SCHEMA_TEXT = """# LLM Wiki — ζ(5) Irrationality via Brown–Zudilin M₀,₈

This wiki is the agent-managed knowledge layer for the `zeta5-autoresearch` repo.

## Core Rules

- `wiki/raw/` is immutable source material.
- The agent may update `wiki/` pages, `wiki/index.md`, `wiki/log.md`, and `wiki/frontier.md`.
- Wiki pages cite only `wiki/raw/...` snapshots.
- All cross-references between pages use `[[wikilinks]]`.
- Every page carries YAML frontmatter with:
  - `title`
  - `category`
  - `phase`
  - `direction`
  - `sources`
  - `last_updated`

## Program Goal

Prove the irrationality of `ζ(5)` using Brown–Zudilin's `M₀,₈` cellular integral framework by constructing an
Apéry-type linear form with exponentially small value relative to denominator growth.

## Banked Program History

- Phase 1: build infrastructure, extract exact objects, run recurrence obstruction campaigns, and hit the exact
  `n = 435` kernel wall.
- Phase 2: freeze the blocked lane, pivot to source-backed decay-side objects, build bridges and transfer objects,
  and map the structural landscape via exact decision gates.

## Operational Rules

- Never cite `data/logs/`, `src/`, or `refs/` directly from the wiki; ingest through `wiki/raw/`.
- Track hard walls and exhausted ansatz classes as carefully as positive results.
- Keep the non-symmetric baseline `P_n` marked as `not source-backed` unless a raw source proves otherwise.
- Treat the Zudilin 2002 recurrence as a calibration anchor, not as the Brown–Zudilin baseline object.
- Treat the six-window normalized Plücker object as the current nonlinear frontier.
"""


@dataclass(frozen=True)
class PageSpec:
    relative_path: str
    title: str
    category: str
    phase: str
    direction: str
    sources: tuple[str, ...]
    summary: str
    body: str


def wiki_root(repo_root: Path) -> Path:
    return repo_root / WIKI_DIRNAME


def raw_root(repo_root: Path) -> Path:
    return wiki_root(repo_root) / RAW_DIRNAME


def ensure_wiki_skeleton(repo_root: Path) -> None:
    root = wiki_root(repo_root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "raw").mkdir(exist_ok=True)
    for raw_name in ("logs", "refs", "code"):
        (root / "raw" / raw_name).mkdir(parents=True, exist_ok=True)
    for dirname in set(WIKI_CATEGORY_DIRS.values()):
        if dirname:
            (root / dirname).mkdir(parents=True, exist_ok=True)


def write_schema(repo_root: Path) -> Path:
    path = wiki_root(repo_root) / "schema.md"
    path.write_text(SCHEMA_TEXT, encoding="utf-8")
    return path


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def page_name_from_path(page_path: Path) -> str:
    if page_path.name == "frontier.md":
        return "frontier"
    if page_path.name == "index.md":
        return "index"
    if page_path.name == "log.md":
        return "log"
    if page_path.name == "schema.md":
        return "schema"
    return page_path.stem


def parse_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    _, rest = markdown.split("---\n", 1)
    frontmatter_text, body = rest.split("\n---\n", 1)
    return yaml.safe_load(frontmatter_text) or {}, body


def write_page(repo_root: Path, spec: PageSpec) -> Path:
    path = wiki_root(repo_root) / spec.relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = {
        "title": spec.title,
        "category": spec.category,
        "phase": spec.phase,
        "direction": spec.direction,
        "sources": list(spec.sources),
        "last_updated": datetime.now().strftime(DATE_FMT),
    }
    payload = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        spec.summary,
        "",
        spec.body.strip(),
        "",
    ]
    path.write_text("\n".join(payload), encoding="utf-8")
    return path


def source_title_from_text(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ")


def stable_snapshot_destination(source_path: Path, destination_root: Path) -> Path:
    destination = destination_root / source_path.name
    if not destination.exists():
        return destination
    if destination.read_bytes() == source_path.read_bytes():
        return destination
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return destination_root / f"{source_path.stem}__{timestamp}{source_path.suffix}"


def snapshot_source(source_path: Path, destination_root: Path) -> Path:
    destination = stable_snapshot_destination(source_path=source_path, destination_root=destination_root)
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
    return destination


def snapshot_logs(repo_root: Path) -> tuple[Path, ...]:
    source_dir = repo_root / "data" / "logs"
    destination_root = raw_root(repo_root) / "logs"
    return tuple(snapshot_source(path, destination_root) for path in sorted(source_dir.glob("*.md")))


def snapshot_refs(repo_root: Path) -> tuple[Path, ...]:
    source_dir = repo_root / "refs"
    destination_root = raw_root(repo_root) / "refs"
    return tuple(snapshot_source(path, destination_root) for path in sorted(source_dir.glob("*.md")))


def snapshot_code(repo_root: Path) -> tuple[Path, ...]:
    destination_root = raw_root(repo_root) / "code"
    snapshots: list[Path] = []
    for relative in KEY_CODE_SNAPSHOTS:
        snapshots.append(snapshot_source(repo_root / relative, destination_root))
    return tuple(snapshots)


def infer_phase_and_direction(name: str) -> tuple[str, str]:
    stem = name.lower()
    if "phase2" in stem:
        phase = "2"
    else:
        phase = "1"

    direction_rules: tuple[tuple[str, str], ...] = (
        ("baseline_extraction", "10"),
        ("baseline_odd", "10"),
        ("baseline_full_packet", "10"),
        ("symmetric_source_packet", "11"),
        ("symmetric_baseline_transfer", "12"),
        ("symmetric_dual_baseline_transfer", "12"),
        ("annihilator_transfer", "12"),
        ("chart_transfer", "13"),
        ("normalized_plucker", "13"),
        ("plucker_quotient", "13"),
        ("six_window_plucker", "13"),
        ("six_chart", "13"),
        ("zudilin_2002", "9"),
        ("literature_verification", "8"),
        ("construction_memo", "8"),
        ("baseline_decay_audit", "7"),
        ("baseline_decay_bridge", "7"),
        ("pivot_report", "7"),
        ("dual_companion_checkpoint", "7"),
        ("baseline_recurrence", "3"),
        ("baseline_modular_family_survey", "3"),
        ("baseline_shift_catalog_survey", "3"),
        ("baseline_shift_catalog_survey_wide", "3"),
        ("dual_f7_companion_normalization", "5"),
        ("dual_f7_companion_recurrence", "5"),
        ("dual_f7_exact_probe", "4"),
        ("dual_f7_probe", "4"),
        ("dual_f7_zeta5_probe", "4"),
        ("dual_f7_zeta5_growth", "4"),
        ("dual_f7_zeta5_modular_recurrence", "4"),
        ("dual_f7_zeta5_shift_catalog_survey", "4"),
        ("kernel", "6"),
    )
    for token, direction in direction_rules:
        if token in stem:
            return phase, direction
    if stem.startswith("bz_baseline"):
        return phase, "2"
    if stem.startswith("bz_dual_f7"):
        return phase, "4"
    if stem.startswith("bz_totally_symmetric"):
        return phase, "11"
    return phase, "frontier"


def source_summary_for_raw(raw_file: Path, repo_root: Path) -> PageSpec:
    relative_raw = raw_file.relative_to(wiki_root(repo_root)).as_posix()
    text = raw_file.read_text(encoding="utf-8")
    title = source_title_from_text(raw_file, text)
    phase, direction = infer_phase_and_direction(raw_file.stem)
    kind = raw_file.parent.name
    summary = f"Source snapshot for `{relative_raw}`."
    bullets: list[str] = [
        f"- Raw snapshot: `{relative_raw}`",
        f"- Source kind: `{kind}`",
        f"- Phase tag: `{phase}`",
        f"- Direction tag: `{direction}`",
    ]
    if kind == "logs":
        if "decision_gate" in raw_file.stem:
            bullets.append("- This raw source records a decision gate or hard wall.")
        elif "probe" in raw_file.stem:
            bullets.append("- This raw source records a probe or screen result.")
        elif "report" in raw_file.stem:
            bullets.append("- This raw source records a report or checkpoint artifact.")
    elif kind == "refs":
        bullets.append("- This raw source is a local literature note snapshot.")
    elif kind == "code":
        bullets.append("- This raw source is a code snapshot used by wiki code pages.")
    body = "\n".join(
        [
            "## Snapshot role",
            "",
            *bullets,
            "",
            "## Extracted heading",
            "",
            f"- `{title}`",
            "",
            "## Wiki use",
            "",
            "This page exists so synthesis pages can cite an immutable raw snapshot rather than live repo paths.",
        ]
    )
    page_name = slugify(raw_file.stem)
    return PageSpec(
        relative_path=f"sources/{page_name}.md",
        title=title,
        category="source",
        phase=phase,
        direction=direction,
        sources=(relative_raw,),
        summary=summary,
        body=body,
    )


def all_raw_snapshots(repo_root: Path) -> tuple[Path, ...]:
    root = raw_root(repo_root)
    return tuple(sorted(path for path in root.rglob("*") if path.is_file()))


def build_core_pages(repo_root: Path) -> tuple[PageSpec, ...]:
    return (
        PageSpec(
            relative_path="frontier.md",
            title="Research Frontier",
            category="frontier",
            phase="2",
            direction="frontier",
            sources=(
                "raw/logs/bz_dual_f7_companion_normalization_report.md",
                "raw/logs/bz_phase2_dual_companion_checkpoint.md",
                "raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Current live frontier: frozen exact-side obstruction through degree 106, plus the six-window normalized Plücker nonlinear frontier.",
            body="""
## Current live frontier

- Exact-side frozen frontier: dual companion caches banked through `n=434`, with the exact cleared-window
  `(1,0,-1,-2)` recurrence family ruled out through degree `106` on window `n<=431`.
- Current nonlinear frontier: the [[six-window-normalized-plucker-object]] is the strongest surviving transfer object.

## Active interpretation

- The old exact lane is [[exact-side-frozen-frontier|frozen]], not active.
- The strongest live object is the six-window normalized Plücker invariant, not any quotient of it.
- The next defensible move is a different recurrence-level family on that six-window object, not another quotient or
  support-depth escalation.

## Related pages

- [[exact-side-frozen-frontier]]
- [[six-window-normalized-plucker-object]]
- [[exhausted-ansatz-classes]]
- [[completed-directions]]
""",
        ),
        PageSpec(
            relative_path="audits/completed-directions.md",
            title="Completed Directions",
            category="audit",
            phase="2",
            direction="frontier",
            sources=(
                "raw/logs/bz_phase2_pivot_report.md",
                "raw/logs/bz_phase2_construction_memo.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Program-level ledger of directions 1–13 and their banked outcome or hard wall.",
            body="""
## Summary

The completed program currently has thirteen numbered directions, grouped into:

- Phase 1: infrastructure, exact extraction, recurrence obstruction, and the `n=435` kernel wall.
- Phase 2: decay-side pivot, literature verification, bridge calibration, packet extraction, transfer objects, and
  nonlinear window-geometry screens.

## Direction ledger

1. Infrastructure and exact-arithmetic workflow: banked.
2. Baseline `Q_n` denominator-side study: banked.
3. Low-complexity baseline recurrence obstruction: hard wall.
4. Dual `F_7` exact coefficient extraction: banked.
5. Dual companion recurrence program: hard wall at degree `106`.
6. Kernel-engineering marathon to reach `n=435`: frozen architectural wall.
7. Phase-2 pivot and decay audit: banked.
8. Literature verification and construction memo: banked.
9. Zudilin 2002 bridge stack: hard wall; low-complexity bridge ansätze exhausted.
10. Baseline extraction on multiple packet choices: hard wall.
11. Symmetric source packet compression: hard wall.
12. Transfer-object ladder: hard wall.
13. Nonlinear window-geometry objects: current frontier.

## Use

Every new finished direction should extend this page and the exhausted ansatz table before another nearby lane is tried.
""",
        ),
        PageSpec(
            relative_path="conclusions/exhausted-ansatz-classes.md",
            title="Exhausted Ansatz Classes",
            category="conclusion",
            phase="2",
            direction="frontier",
            sources=(
                "raw/logs/bz_phase2_literature_verification_report.md",
                "raw/logs/bz_phase2_plucker_quotient_family_screen.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Tracked ledger of ansatz classes that should not be retried without a new structural reason.",
            body="""
## Exhausted classes

- Low-order / low-degree recurrence families on baseline `Q_n`.
- Dual companion `(1,0,-1,-2)` polynomial recurrence family through degree `106`.
- Zudilin-bridge scalar normalization maps.
- Zudilin-bridge affine normalization maps.
- Zudilin-bridge quadratic normalization maps.
- Zudilin-bridge constant coupled `2x2` map.
- Baseline packet compression on `(constant, ζ(5))`, `(ζ(5), ζ(3))`, and full packet.
- Symmetric source packet compression.
- Symmetric-to-baseline and symmetric-dual-to-baseline-dual low-complexity transfer maps.
- Local annihilator transfer maps in the same bounded family.
- Plücker quotient and cross-ratio quotient families.

## Rule

Do not retry any class above unless a new source-backed identity, symmetry, or recurrence-level reason changes the
object itself rather than merely enlarging the same fit family.
""",
        ),
        PageSpec(
            relative_path="concepts/bounded-refinement-ladder.md",
            title="Bounded Refinement Ladder",
            category="concept",
            phase="2",
            direction="frontier",
            sources=(
                "raw/logs/bz_phase2_baseline_residual_refinement_decision_gate.md",
                "raw/logs/bz_phase2_baseline_odd_residual_refinement_decision_gate.md",
                "raw/logs/bz_phase2_baseline_full_packet_compression_decision_gate.md",
            ),
            summary="The recurring same-index -> difference -> lagged-support pattern that marks a structural wall across packet and transfer directions.",
            body="""
## Pattern

Across packet compression, transfer, and refinement directions, the same bounded ladder recurs:

1. same-index support-0 family
2. consecutive-difference family
3. lagged support family

The direction either:

- fails right after its fit block, or
- becomes ill-posed at the first richer support level.

## Interpretation

When a new direction hits this pattern, the safe default is to classify it as the same structural obstruction rather
than escalating degree/support mechanically.

## Related pages

- [[exhausted-ansatz-classes]]
- [[six-window-normalized-plucker-object]]
""",
        ),
        PageSpec(
            relative_path="computation/exact-side-frozen-frontier.md",
            title="Exact-Side Frozen Frontier",
            category="computation",
            phase="1",
            direction="5",
            sources=(
                "raw/logs/bz_dual_f7_companion_normalization_report.md",
                "raw/logs/bz_phase2_dual_companion_checkpoint.md",
            ),
            summary="Frozen exact frontier on the dual companion lane: caches to n=434, certified obstruction through degree 106 on n<=431.",
            body="""
## Certified result

- Dual companion caches are banked through `n=434`.
- No nontrivial `(1,0,-1,-2)` polynomial recurrence exists through degree `106`.
- The certified exact window is `n<=431`.

## Status

This lane is frozen, not active. The `n=435` step was blocked after multiple kernel redesigns in [[bz-dual-f7-extractor]].
""",
        ),
        PageSpec(
            relative_path="computation/six-window-normalized-plucker-frontier.md",
            title="Six-Window Normalized Plucker Frontier",
            category="computation",
            phase="2",
            direction="13",
            sources=(
                "raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md",
                "raw/logs/bz_phase2_plucker_quotient_family_screen.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Current nonlinear frontier: the full six-window normalized Plücker object improves the cheap frontier, while quotient continuations weaken it.",
            body="""
## Screen summary

- Five-term normalized Plücker object improved the old chart frontier to `10, 11, 20, 30, 40`.
- Quotient and cross-ratio variants on the five-term object were weaker.
- Full six-window normalized Plücker improved the cheap frontier again to `20, 21`.
- The six-window projective quotient dropped back to `19, 20`.
- The first richer support family on the full six-window object is ill-posed.

## Reading

The live promise is in the full wider-window invariant, not in its projective quotients.
""",
        ),
        PageSpec(
            relative_path="entities/baseline-qn.md",
            title="Baseline Q_n",
            category="entity",
            phase="1",
            direction="2",
            sources=(
                "raw/logs/bz_baseline_recurrence_report.md",
                "raw/logs/bz_baseline_modular_family_survey_report.md",
            ),
            summary="Baseline denominator-side sequence accessible directly from the Brown–Zudilin baseline family.",
            body="""
## Role

`Q_n` is the baseline denominator-side sequence and the earliest direct object studied in the program.

## Status

- Source-backed as a computation target.
- Extensively screened for low-complexity recurrence structure.
- Important for growth and denominator-side comparisons, but not itself the missing non-symmetric decay object.
""",
        ),
        PageSpec(
            relative_path="entities/non-symmetric-baseline-pn.md",
            title="Non-Symmetric Baseline P_n",
            category="entity",
            phase="2",
            direction="8",
            sources=(
                "raw/logs/bz_phase2_literature_verification_report.md",
                "raw/refs/notes_bz_2026.md",
            ),
            summary="The baseline non-symmetric decay-side numerator/remainder object; explicitly not source-backed in the checked literature.",
            body="""
## Status

This object is **not source-backed** in the checked primary-source neighborhood.

- Brown–Zudilin gives explicit symmetric decay-side data.
- The checked sources do not give an explicit non-symmetric baseline `P_n` sequence or recurrence.

## Rule

Never treat this object as explicitly known in the wiki.
""",
        ),
        PageSpec(
            relative_path="entities/dual-f7-object.md",
            title="Dual F7 Object",
            category="entity",
            phase="1",
            direction="4",
            sources=(
                "raw/code/bz_dual_f7.py",
                "raw/logs/bz_dual_f7_exact_probe_report.md",
            ),
            summary="The exact dual-side extraction object whose coefficient channels drive the companion and packet programs.",
            body="""
## Definition

The dual `F_7` object is extracted by [[bz-dual-f7-extractor]] and decomposed into exact coefficient channels.

## Channels

- constant term
- `ζ(3)` coefficient
- `ζ(5)` coefficient

These channels feed the dual companion, packet, and transfer experiments.
""",
        ),
        PageSpec(
            relative_path="entities/coefficient-channels.md",
            title="Coefficient Channels",
            category="entity",
            phase="1",
            direction="4",
            sources=(
                "raw/logs/bz_dual_f7_probe_report.md",
                "raw/logs/bz_dual_f7_zeta5_probe_report.md",
            ),
            summary="The three exact dual F7 coefficient channels: constant term, ζ(3), and ζ(5).",
            body="""
## Channel list

- constant channel: rational component
- `ζ(3)` channel
- `ζ(5)` channel

These are the atomic exact objects behind packet construction and dual companion sequences.
""",
        ),
        PageSpec(
            relative_path="entities/dual-companion-sequences.md",
            title="Dual Companion Sequences",
            category="entity",
            phase="1",
            direction="5",
            sources=(
                "raw/logs/bz_dual_f7_companion_probe_report.md",
                "raw/logs/bz_dual_f7_companion_normalization_report.md",
            ),
            summary="Derived exact dual-side companion sequences used in the main exact recurrence obstruction program.",
            body="""
## Status

These sequences drove the main exact companion normalization campaign and produced the strongest exact obstruction
certificate currently banked in the repo.
""",
        ),
        PageSpec(
            relative_path="entities/symmetric-scaled-triple.md",
            title="Symmetric Scaled Triple",
            category="entity",
            phase="2",
            direction="11",
            sources=(
                "raw/logs/bz_totally_symmetric_linear_forms_report.md",
                "raw/logs/bz_phase2_symmetric_source_packet_object_spec.md",
            ),
            summary="The source-backed symmetric decay anchor: (d_n^5 Q_n, d_n^5 P_n, d_n^2 d_{2n} P̂_n).",
            body="""
## Role

This is the safest source-backed decay-side anchor in the repo and the entry point for symmetric compression and
transfer experiments.
""",
        ),
        PageSpec(
            relative_path="entities/zudilin-2002-bridge.md",
            title="Zudilin 2002 Bridge",
            category="entity",
            phase="2",
            direction="9",
            sources=(
                "raw/logs/bz_phase2_zudilin_2002_bridge_probe.md",
                "raw/logs/bz_phase2_external_bridge_spec.md",
            ),
            summary="The explicit recurrence bridge object used for calibration, not as the Brown–Zudilin target itself.",
            body="""
## Role

The Zudilin 2002 recurrence is a calibration anchor with explicit channels and recurrence data.

## Constraint

It is not the Brown–Zudilin baseline object, and several low-complexity bridge ansatz classes against it are already
[[exhausted-ansatz-classes|exhausted]].
""",
        ),
        PageSpec(
            relative_path="entities/six-window-normalized-plucker-object.md",
            title="Six-Window Normalized Plucker Object",
            category="entity",
            phase="2",
            direction="13",
            sources=(
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
                "raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md",
            ),
            summary="Current strongest surviving nonlinear transfer object, built from six-term packet windows in normalized Plücker coordinates.",
            body="""
## Status

This is the current best surviving object class.

- It improves the cheap frontier beyond the five-term normalized Plücker object.
- Its quotient continuation is weaker.
- Its first richer support family is ill-posed rather than predictive.

## Next move

Try a different recurrence-level family on this object, not another quotient or support-depth escalation.
""",
        ),
        PageSpec(
            relative_path="concepts/apery-type-linear-forms.md",
            title="Apery-Type Linear Forms",
            category="concept",
            phase="1",
            direction="frontier",
            sources=("raw/logs/bz_phase2_construction_memo.md",),
            summary="Classical target shape L_n = a_n ζ(5) − b_n with denominator growth beaten by decay.",
            body="""
The program goal is to find an Apéry-type linear form with enough decay relative to denominator growth to force the
irrationality of `ζ(5)`.
""",
        ),
        PageSpec(
            relative_path="concepts/worthiness-exponent.md",
            title="Worthiness Exponent",
            category="concept",
            phase="2",
            direction="8",
            sources=(
                "raw/logs/bz_phase2_literature_verification_report.md",
                "raw/refs/notes_bz_2026.md",
            ),
            summary="Ratio comparing linear-form decay to denominator growth; the decisive quantity for irrationality-style usefulness.",
            body="""
The worthiness exponent measures whether the linear form shrinks faster than the denominator side grows. It is one of
the main conceptual filters for deciding whether a construction is proof-relevant or only structurally interesting.
""",
        ),
        PageSpec(
            relative_path="concepts/packet-objects.md",
            title="Packet Objects",
            category="concept",
            phase="2",
            direction="10",
            sources=(
                "raw/logs/bz_phase2_baseline_pair_object_spec.md",
                "raw/logs/bz_phase2_baseline_odd_pair_object_spec.md",
                "raw/logs/bz_phase2_baseline_full_packet_object_spec.md",
            ),
            summary="Multi-channel baseline objects assembled from the dual F7 coefficient channels for extraction and transfer experiments.",
            body="""
Packet objects promote selected channel tuples to the active object and treat the remaining channel as residual or
carry the full triple together. Several packet choices were tried and all hit the bounded refinement ladder.
""",
        ),
        PageSpec(
            relative_path="concepts/transfer-maps.md",
            title="Transfer Maps",
            category="concept",
            phase="2",
            direction="12",
            sources=(
                "raw/logs/bz_phase2_symmetric_baseline_transfer_decision_gate.md",
                "raw/logs/bz_phase2_symmetric_dual_baseline_transfer_decision_gate.md",
            ),
            summary="Low-complexity maps between symmetric and baseline packet objects; all banked transfer ladders currently stall.",
            body="""
Transfer maps try to move structure from source-backed symmetric objects into the baseline lane. The current banked
result is that all natural low-complexity packet transfer families stall.
""",
        ),
        PageSpec(
            relative_path="concepts/annihilator-profiles.md",
            title="Annihilator Profiles",
            category="concept",
            phase="2",
            direction="12",
            sources=("raw/logs/bz_phase2_symmetric_dual_baseline_annihilator_transfer_decision_gate.md",),
            summary="Local recurrence-profile objects derived from packet windows; useful as recurrence-level invariants but not yet a successful transfer object.",
            body="""
Annihilator profiles lift packet data into local recurrence coefficients. They did not beat the full-packet transfer
object in the current bounded family.
""",
        ),
        PageSpec(
            relative_path="concepts/normalized-plucker-geometry.md",
            title="Normalized Plucker Geometry",
            category="concept",
            phase="2",
            direction="13",
            sources=(
                "raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Grassmannian-style window invariants built from packet windows; the strongest nonlinear direction tried so far.",
            body="""
Normalized Plücker objects track subspace geometry of packet windows in a nonlinear, projectively meaningful way. This
family produced the first clear frontier improvements beyond packet and transfer maps.
""",
        ),
        PageSpec(
            relative_path="concepts/decision-gate-methodology.md",
            title="Decision-Gate Methodology",
            category="concept",
            phase="2",
            direction="frontier",
            sources=(
                "raw/logs/bz_phase2_pivot_report.md",
                "raw/code/baseline_residual_refinement_decision_gate.py",
                "raw/code/symmetric_dual_baseline_chart_transfer_decision_gate.py",
            ),
            summary="Program rule that every bounded lane must end in an explicit banked outcome, hard wall, or frontier recommendation.",
            body="""
Decision gates record:

- object tested
- parameter range
- family class
- exact window size
- failure mode or certified outcome

This prevents the repo from re-deriving the same dead ends and is one of the main positive outputs of the program.
""",
        ),
        PageSpec(
            relative_path="code/bz-dual-f7-extractor.md",
            title="bz_dual_f7.py Extractor and Kernel History",
            category="code",
            phase="1",
            direction="6",
            sources=(
                "raw/code/bz_dual_f7.py",
                "raw/logs/bz_phase2_dual_companion_checkpoint.md",
            ),
            summary="Code page for the core exact dual F7 extractor and the six-round kernel-engineering history behind the frozen n=435 wall.",
            body="""
## Role

[`bz_dual_f7.py`] is the core exact extractor for dual `F_7` coefficient channels.

## History

The repo banked multiple kernel redesigns here: factorized rational paths, backend `mpq` fast paths, component
accumulators, reduced-fraction helpers, fused extraction logic, and hot-loop rewrites.

## Current status

The `n=435` wall is treated as architectural, not as a “one more micro-optimization” problem.
""",
        ),
        PageSpec(
            relative_path="code/cache-system.md",
            title="Cache System",
            category="code",
            phase="1",
            direction="4",
            sources=(
                "raw/code/dual_f7_exact_coefficient_cache.py",
                "raw/logs/bz_dual_f7_exact_probe_report.md",
            ),
            summary="Code page for exact cache management of the dual coefficient channels and companion objects.",
            body="""
The cache system stores exact channel data and derived probe outputs so exact windows can be reused without recomputing
the whole extraction stack.
""",
        ),
        PageSpec(
            relative_path="code/orchestration-and-filters.md",
            title="Orchestration and Structural Filters",
            category="code",
            phase="1",
            direction="1",
            sources=(
                "raw/code/orchestrator.py",
                "raw/code/gate0_parse.py",
                "raw/code/gate1_filter.py",
            ),
            summary="Code page for the structural orchestration layer and the early filter gates that keep the search conservative.",
            body="""
These modules hold the non-notebook workflow together: parse input seeds, filter structural candidates, and route
them into exact or modular probe campaigns.
""",
        ),
        PageSpec(
            relative_path="code/symmetric-decay-anchor.md",
            title="Symmetric Decay Anchor Code",
            category="code",
            phase="2",
            direction="11",
            sources=(
                "raw/code/bz_symmetric_linear_forms_probe.py",
                "raw/logs/bz_totally_symmetric_linear_forms_report.md",
            ),
            summary="Code page for the source-backed totally symmetric linear-form pipeline used as the main decay-side anchor.",
            body="""
This pipeline provides the source-backed symmetric triple and anchors the symmetric compression and transfer stages of
the phase-2 program.
""",
        ),
        PageSpec(
            relative_path="code/decision-gate-artifacts.md",
            title="Decision-Gate Artifact Writers",
            category="code",
            phase="2",
            direction="frontier",
            sources=(
                "raw/code/campaign_report.py",
                "raw/code/baseline_residual_refinement_decision_gate.py",
                "raw/code/symmetric_dual_baseline_chart_transfer_decision_gate.py",
            ),
            summary="Code page for the report-writing pattern that turns every probe family into a traceable gate or checkpoint artifact.",
            body="""
These modules exemplify the repo-native pattern: generate exact outputs, write markdown and JSON artifacts, and bank
hard walls in a way that the wiki can ingest cleanly.
""",
        ),
        PageSpec(
            relative_path="literature/brown-zudilin-2210-03391v3.md",
            title="Brown–Zudilin 2210.03391v3",
            category="literature",
            phase="2",
            direction="8",
            sources=(
                "raw/refs/notes_bz_2026.md",
                "raw/logs/bz_phase2_literature_verification_report.md",
            ),
            summary="Primary-source page for the foundational Brown–Zudilin paper: symmetric data yes, explicit non-symmetric baseline P_n no.",
            body="""
## Provides

- `M₀,₈` cellular integral framework
- explicit symmetric decay-side data
- symmetric recurrences

## Does not provide

- explicit non-symmetric baseline `P_n`
- explicit non-symmetric baseline recurrence
- direct dual `F_7` object
""",
        ),
        PageSpec(
            relative_path="literature/zudilin-2002.md",
            title="Zudilin 2002",
            category="literature",
            phase="2",
            direction="9",
            sources=(
                "raw/logs/bz_phase2_zudilin_2002_bridge_probe.md",
                "raw/logs/bz_phase2_literature_verification_report.md",
            ),
            summary="Bridge-source page for the explicit Zudilin 2002 recurrence used as calibration, not as the Brown–Zudilin target.",
            body="""
Zudilin 2002 supplies a recurrence-explicit bridge object with explicit `ζ(5)` and companion channels. It is useful
for calibration and normalization checks, but it does not close the gap to the Brown–Zudilin non-symmetric baseline.
""",
        ),
        PageSpec(
            relative_path="conclusions/obstruction-is-not-normalization.md",
            title="Obstruction Is Not Normalization",
            category="conclusion",
            phase="2",
            direction="9",
            sources=("raw/logs/bz_phase2_zudilin_2002_normalization_decision_gate.md",),
            summary="Banked conclusion: the obstruction survives multiple normalization-map families.",
            body="Scalar, affine, quadratic, and coupled constant normalization-map families are exhausted. The obstruction is not a simple normalization mismatch.",
        ),
        PageSpec(
            relative_path="conclusions/obstruction-is-not-packet-choice.md",
            title="Obstruction Is Not Packet Choice",
            category="conclusion",
            phase="2",
            direction="10",
            sources=("raw/logs/bz_phase2_baseline_full_packet_compression_decision_gate.md",),
            summary="Banked conclusion: changing between the natural baseline packet choices does not remove the wall.",
            body="The `(constant, ζ(5))`, `(ζ(5), ζ(3))`, and full packet choices all hit the same bounded refinement obstruction.",
        ),
        PageSpec(
            relative_path="conclusions/obstruction-survives-transfer.md",
            title="Obstruction Survives Transfer",
            category="conclusion",
            phase="2",
            direction="12",
            sources=(
                "raw/logs/bz_phase2_symmetric_baseline_transfer_decision_gate.md",
                "raw/logs/bz_phase2_symmetric_dual_baseline_transfer_decision_gate.md",
            ),
            summary="Banked conclusion: low-complexity symmetric-to-baseline transfer families do not break the obstruction.",
            body="The obstruction survives symmetric-source to baseline transfer, symmetric-dual to baseline-dual transfer, and local annihilator transfer objects.",
        ),
        PageSpec(
            relative_path="conclusions/quotient-invariants-are-weaker.md",
            title="Quotient Invariants Are Weaker",
            category="conclusion",
            phase="2",
            direction="13",
            sources=(
                "raw/logs/bz_phase2_plucker_quotient_family_screen.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Banked conclusion: projective and cross-ratio quotient variants are systematically weaker than the full normalized invariants.",
            body="Both five-term and six-term quotient screens underperform the corresponding full normalized Plücker objects.",
        ),
        PageSpec(
            relative_path="conclusions/bounded-refinement-ladder-is-universal.md",
            title="Bounded Refinement Ladder Is Universal",
            category="conclusion",
            phase="2",
            direction="frontier",
            sources=(
                "raw/logs/bz_phase2_baseline_residual_refinement_decision_gate.md",
                "raw/logs/bz_phase2_symmetric_source_packet_compression_decision_gate.md",
            ),
            summary="Banked conclusion: the same bounded refinement pattern recurs across packet and transfer directions.",
            body="When a new lane reproduces the same ladder, it should be classified as the same structural wall rather than escalated mechanically.",
        ),
        PageSpec(
            relative_path="conclusions/non-symmetric-baseline-pn-not-source-backed.md",
            title="Non-Symmetric Baseline P_n Is Not Source-Backed",
            category="conclusion",
            phase="2",
            direction="8",
            sources=("raw/logs/bz_phase2_literature_verification_report.md",),
            summary="Banked conclusion: the explicit non-symmetric baseline P_n is not source-backed in the checked primary-source neighborhood.",
            body="This conclusion should be enforced everywhere the baseline `P_n` is mentioned.",
        ),
        PageSpec(
            relative_path="conclusions/wider-window-nonlinear-invariants-improve-the-frontier.md",
            title="Wider-Window Nonlinear Invariants Improve the Frontier",
            category="conclusion",
            phase="2",
            direction="13",
            sources=(
                "raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md",
                "raw/logs/bz_phase2_six_window_plucker_followup_screen.md",
            ),
            summary="Banked conclusion: the only direction that materially improved the frontier was moving to wider-window nonlinear Plücker/subspace geometry.",
            body="This is the strongest positive structural conclusion of the late phase-2 program.",
        ),
        PageSpec(
            relative_path="conclusions/exact-n435-wall-is-architectural.md",
            title="Exact n=435 Wall Is Architectural",
            category="conclusion",
            phase="1",
            direction="6",
            sources=("raw/logs/bz_phase2_dual_companion_checkpoint.md",),
            summary="Banked conclusion: the blocked n=435 step is architectural, not a missing micro-optimization.",
            body="The phase-2 pivot exists because six rounds of kernel engineering did not convert the `n=435` barrier into a routine exact extension.",
        ),
    )


def build_index(repo_root: Path) -> Path:
    root = wiki_root(repo_root)
    page_paths = sorted(
        path
        for path in root.rglob("*.md")
        if path.name not in {"index.md", "log.md"}
    )
    grouped: dict[str, list[tuple[str, str, str]]] = {}
    for path in page_paths:
        relative = path.relative_to(root)
        if relative.parts[:1] == ("raw",):
            continue
        if relative.name == "schema.md":
            continue
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        category = str(metadata.get("category", "uncategorized"))
        title = str(metadata.get("title", page_name_from_path(path)))
        summary = ""
        for line in body.splitlines():
            if line.strip():
                summary = line.strip()
                break
        grouped.setdefault(category, []).append((title, relative.as_posix(), summary))

    lines = [
        "# Wiki Index",
        "",
        "Start with [[frontier]] for the current program state, then drill into category pages and source summaries.",
        "",
    ]
    for category in sorted(grouped):
        lines.append(f"## {category.title()}")
        lines.append("")
        for title, relative, summary in grouped[category]:
            lines.append(f"- [{title}]({relative}) — {summary}")
        lines.append("")
    path = root / "index.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def append_log_entry(repo_root: Path, *, kind: str, title: str) -> Path:
    path = wiki_root(repo_root) / "log.md"
    if path.exists():
        existing = path.read_text(encoding="utf-8").rstrip()
        lines = [existing, ""]
    else:
        lines = ["# Wiki Log", ""]
    stamp = datetime.now().strftime(DATE_FMT)
    lines.extend((f"## [{stamp}] {kind} | {title}", ""))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def lint_wiki(repo_root: Path) -> list[str]:
    issues: list[str] = []
    root = wiki_root(repo_root)
    if not root.exists():
        return ["wiki directory does not exist"]

    page_paths = sorted(path for path in root.rglob("*.md") if path.relative_to(root).parts[:1] != ("raw",))
    page_names = {page_name_from_path(path): path for path in page_paths}
    backlinks: dict[str, set[str]] = {name: set() for name in page_names}

    for path in page_paths:
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        if path.name not in {"index.md", "log.md", "schema.md"}:
            required = {"title", "category", "phase", "direction", "sources", "last_updated"}
            missing = sorted(required - set(metadata))
            if missing:
                issues.append(f"{path.relative_to(root)} missing frontmatter keys: {', '.join(missing)}")
            sources = metadata.get("sources", [])
            if not isinstance(sources, list) or any(not str(item).startswith("raw/") for item in sources):
                issues.append(f"{path.relative_to(root)} has non-raw sources")
        for match in re.findall(r"\[\[([^\]]+)\]\]", body):
            target = slugify(match)
            if target in backlinks:
                backlinks[target].add(page_name_from_path(path))
        for _, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body):
            target_path = (path.parent / target).resolve()
            try:
                relative_target = target_path.relative_to(root.resolve())
            except ValueError:
                continue
            if relative_target.parts[:1] == ("raw",):
                continue
            target_name = page_name_from_path(root / relative_target)
            if target_name in backlinks:
                backlinks[target_name].add(page_name_from_path(path))

    for name, path in page_names.items():
        if path.name in {"index.md", "log.md", "schema.md", "frontier.md"}:
            continue
        if not backlinks.get(name):
            issues.append(f"orphan page: {path.relative_to(root)}")

    frontier = root / "frontier.md"
    if not frontier.exists():
        issues.append("frontier.md is missing")
    exhausted = root / "conclusions" / "exhausted-ansatz-classes.md"
    if not exhausted.exists():
        issues.append("exhausted ansatz page is missing")
    pn_page = root / "entities" / "non-symmetric-baseline-pn.md"
    if pn_page.exists():
        text = pn_page.read_text(encoding="utf-8").lower()
        if "not source-backed" not in text:
            issues.append("non-symmetric baseline P_n page does not mark the object as not source-backed")
    else:
        issues.append("non-symmetric baseline P_n page is missing")
    return issues


def bootstrap(repo_root: Path) -> None:
    ensure_wiki_skeleton(repo_root)
    write_schema(repo_root)
    snapshot_logs(repo_root)
    snapshot_refs(repo_root)
    snapshot_code(repo_root)

    for raw_file in all_raw_snapshots(repo_root):
        write_page(repo_root, source_summary_for_raw(raw_file, repo_root))
    for page in build_core_pages(repo_root):
        write_page(repo_root, page)

    build_index(repo_root)
    append_log_entry(repo_root, kind="ingest", title="Bootstrap raw logs, refs, code, and core synthesis pages")


def ingest(repo_root: Path, paths: Iterable[str]) -> None:
    ensure_wiki_skeleton(repo_root)
    touched_titles: list[str] = []
    for raw_path in paths:
        source = Path(raw_path)
        if not source.is_absolute():
            source = (repo_root / raw_path).resolve()
        if not source.exists():
            raise FileNotFoundError(source)

        if "data/logs" in source.as_posix():
            destination_root = raw_root(repo_root) / "logs"
        elif "refs/" in source.as_posix():
            destination_root = raw_root(repo_root) / "refs"
        else:
            destination_root = raw_root(repo_root) / "code"
        destination = snapshot_source(source, destination_root)
        write_page(repo_root, source_summary_for_raw(destination, repo_root))
        touched_titles.append(destination.name)

    build_index(repo_root)
    append_log_entry(repo_root, kind="ingest", title=", ".join(touched_titles))


def run_lint(repo_root: Path) -> int:
    issues = lint_wiki(repo_root)
    append_log_entry(repo_root, kind="lint", title="Health Check")
    if issues:
        print("# Wiki lint issues")
        for item in issues:
            print(f"- {item}")
        return 1
    print("Wiki lint clean.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the agent-owned research wiki.")
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("bootstrap")
    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("paths", nargs="+")
    subparsers.add_parser("lint")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()

    if args.command == "bootstrap":
        bootstrap(repo_root)
        return 0
    if args.command == "ingest":
        ingest(repo_root, args.paths)
        return 0
    if args.command == "lint":
        return run_lint(repo_root)
    raise RuntimeError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
