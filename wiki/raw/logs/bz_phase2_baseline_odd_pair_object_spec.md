# Phase 2 baseline odd-pair object spec

- Spec id: `bz_phase2_baseline_odd_pair_object_spec`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Source packet spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_target_spec.md`
- Source packet id: `baseline_dual_f7_exact_coefficient_packet`
- Object label: `Baseline odd-weight pair object`
- Object kind: `baseline_side_exact_odd_pair_with_constant_residual`

## Object semantics

The active baseline-side object is the ordered odd-weight pair `(zeta(5), zeta(3))` drawn from the exact baseline dual F_7 coefficient packet, together with the rational constant term carried as explicit residual structure. This is the smallest repo-native object aligned with the odd-zeta projection viewpoint.

## Rationale

This object is preferred after the `(constant, zeta(5))` line hit a hard wall because it keeps the odd-zeta channels together and demotes the rational constant term to residual structure, which better matches the projection language in the construction memo.

## Components

| component | source component | role | max verified index | exact status |
| --- | --- | --- | --- | --- |
| `retained_zeta5` | `zeta5` | exact zeta(5) coefficient retained as the primary odd-target channel | `80` | `exact` |
| `retained_zeta3` | `zeta3` | exact zeta(3) coefficient retained as the companion odd-weight channel | `434` | `exact` |
| `residual_constant` | `constant` | explicit rational residual carried alongside the odd pair | `434` | `exact` |

## Component notes

- `retained_zeta5`: This remains the shortest verified frontier and therefore caps the shared exact window.
- `retained_zeta3`: Keeping zeta(3) in the retained pair matches the odd-zeta projection framing more directly than treating it as noise.
- `residual_constant`: The constant term is demoted to residual structure rather than retained as part of the active odd-weight pair.

## Extraction output type

- Output id: `baseline_odd_extraction_summary_v1`
- Label: `Bounded baseline odd-pair extraction summary`
- Semantics: A bounded odd-pair extraction summary is a repo-native object produced from the baseline odd pair that may recombine or filter the retained odd channels while keeping the constant residual explicit.
- Non-claim: It is not, by default, a claimed baseline P_n sequence or a proved baseline remainder pipeline.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration for conventions and failure modes. It may not redefine the active odd-pair object or supply hidden identities for it.

## Non-claims

- This spec does not claim that `(zeta(5), zeta(3))` is already the baseline decay object.
- This spec does not eliminate the constant residual.
- This spec does not claim a baseline P_n extraction.

## Recommended next step

Implement the first bounded odd-pair extraction rule and require it to preserve the split between retained odd channels and constant residual structure.
