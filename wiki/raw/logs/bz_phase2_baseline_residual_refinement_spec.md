# Phase 2 baseline residual refinement spec

- Spec id: `bz_phase2_baseline_residual_refinement_spec`
- Source post-probe gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_extraction_post_probe_decision_gate.md`
- Source gate id: `bz_phase2_baseline_extraction_post_probe_decision_gate`
- Source extraction rule: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_extraction_rule.md`
- Source rule id: `bz_phase2_baseline_extraction_rule_v1`
- Shared exact window: `n=1..80`
- Active object: `baseline_pair_object_with_explicit_zeta3_residual`

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration to sanity-check bookkeeping conventions and failure modes. It may not redefine the active baseline object or supply hidden identities for it.

## Fixed family ladder

| family | fit window | validation window | coefficients |
| --- | --- | --- | --- |
| `support0_same_index` | `n=1..2` | `n=1..80` | `a, b` |
| `difference_pair` | `n=2..3` | `n=2..80` | `a, b` |
| `support1_lagged_pair` | `n=2..5` | `n=2..80` | `a0, a1, b0, b1` |

## Family details

### `support0_same_index`

- Label: Same-index support-0 residual recombination
- Statement: `r_n = zeta3_n + a * constant_n + b * zeta5_n`
- Goal: Test whether the residual zeta(3) channel collapses under a same-index exact recombination with the retained pair.

### `difference_pair`

- Label: First-difference pair residual recombination
- Statement: `r_n = zeta3_n + a * (constant_n - constant_{n-1}) + b * (zeta5_n - zeta5_{n-1})`
- Goal: Test whether the residual zeta(3) channel is better described against first differences of the retained pair.

### `support1_lagged_pair`

- Label: Lag-1 support residual recombination
- Statement: `r_n = zeta3_n + a0 * constant_n + a1 * constant_{n-1} + b0 * zeta5_n + b1 * zeta5_{n-1}`
- Goal: Test whether one lag of baseline-side support is enough to reclassify the residual zeta(3) channel.

## Non-goals

- Do not fit any bridge-side object in this refinement ladder.
- Do not enlarge to support-2 or n-dependent families in this tranche.
- Do not claim a baseline P_n extraction from these families alone.

## Recommendation

Run the bounded residual-refinement probe next and let its exact full-window verdict choose between a promoted v2 extraction branch and a hard-wall decision gate.
