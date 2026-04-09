# Phase 2 dual projection target spec

- Target id: `baseline_dual_f7_exact_coefficient_packet`
- Target label: `Baseline dual F_7 exact coefficient packet`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Target kind: `pre_projection_exact_coefficient_packet`

## Projection meaning

This target is the exact displayed-series coefficient packet of the Brown-Zudilin baseline dual F_7 linear form: rational constant term, zeta(3) coefficient, and zeta(5) coefficient. It is the smallest repo-native object that already exists exactly and can honestly feed a later parity/projection step without pretending that a baseline P_n sequence has been extracted.

## Non-claims

- This target is not a published baseline P_n sequence.
- This target is not a proved baseline remainder pipeline.
- This target does not by itself isolate the Brown-Zudilin baseline decay object.

## Source basis

- `Construction memo: /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_construction_memo.md`
- `Dual projection experiment plan: /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_experiment_plan.md`
- `Literature verification report: /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_literature_verification_report.md`

## Components

| component | role | max verified index | exact status | cache path |
| --- | --- | --- | --- | --- |
| `constant` | rational constant term of the exact dual F_7 linear form | `434` | `exact` | `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/cache/bz_baseline_dual_f7_constant_terms.json` |
| `zeta3` | exact zeta(3) coefficient of the dual F_7 linear form | `434` | `exact` | `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/cache/bz_baseline_dual_f7_zeta3_terms.json` |
| `zeta5` | exact zeta(5) coefficient of the dual F_7 linear form | `80` | `exact` | `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/cache/bz_baseline_dual_f7_zeta5_terms.json` |

## Component notes

- `constant`: Extracted by the exact dual F_7 linear-form path and cached as canonical rationals. This is the strongest exact baseline companion lane currently banked.
- `zeta3`: Extracted alongside the constant term from the exact dual F_7 linear-form path and cached as canonical rationals.
- `zeta5`: Available from the faster zeta(5)-only exact extractor. Its verified frontier is shorter than the constant/zeta(3) companion caches, so any first projection probe must state that asymmetry explicitly.

## Recommended use

Use this exact coefficient packet as the first bounded projection target. A projection experiment may recombine or filter these three exact components, but it must preserve the distinction between pre-projection coefficient data and any claimed baseline decay sequence.
