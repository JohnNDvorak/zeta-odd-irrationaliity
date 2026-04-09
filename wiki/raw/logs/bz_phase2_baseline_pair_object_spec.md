# Phase 2 baseline pair object spec

- Spec id: `bz_phase2_baseline_pair_object_spec`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Extraction implementation plan: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_extraction_implementation_plan.md`
- Source packet spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_target_spec.md`
- Source packet id: `baseline_dual_f7_exact_coefficient_packet`
- Object label: `Baseline extraction pair object`
- Object kind: `baseline_side_exact_pair_with_explicit_residual`

## Object semantics

The active baseline-side extraction object is the ordered pair `(constant, zeta(5))` drawn from the exact baseline dual F_7 coefficient packet, together with the explicit residual `zeta(3)` channel carried as side information. This is a baseline-native extraction object, not a bridge-fit surrogate.

## Components

| component | source component | role | max verified index | exact status |
| --- | --- | --- | --- | --- |
| `retained_constant` | `constant` | rational constant term retained in the active extraction pair | `434` | `exact` |
| `retained_zeta5` | `zeta5` | exact zeta(5) coefficient retained in the active extraction pair | `80` | `exact` |
| `residual_zeta3` | `zeta3` | explicit residual companion channel carried alongside the retained pair | `434` | `exact` |

## Component notes

- `retained_constant`: This is retained because the current baseline packet already stabilizes it exactly and it pairs naturally with the zeta(5) coefficient.
- `retained_zeta5`: This is the odd-target component of primary proof interest, but its verified window is currently the shortest component frontier.
- `residual_zeta3`: This remains explicit to prevent accidental collapse back into one-channel extraction rhetoric.

## Extraction output type

- Output id: `baseline_extraction_summary_v1`
- Label: `Bounded baseline extraction summary`
- Semantics: A bounded extraction summary is a repo-native object produced from the baseline pair object that may recombine or filter the retained pair while recording the unresolved residual channel explicitly.
- Non-claim: It is not, by default, a claimed baseline P_n sequence or a proved baseline remainder pipeline.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only to sanity-check bookkeeping conventions and failure modes. It may not redefine the active baseline object or supply hidden identities for it.

## Non-claims

- This spec does not claim that `(constant, zeta(5))` is the unique correct baseline extraction object.
- This spec does not eliminate the residual `zeta(3)` channel.
- This spec does not claim a baseline P_n extraction.

## Recommended next step

Implement one bounded extraction rule on this baseline pair object and require the output to distinguish retained output from residual unresolved structure.
