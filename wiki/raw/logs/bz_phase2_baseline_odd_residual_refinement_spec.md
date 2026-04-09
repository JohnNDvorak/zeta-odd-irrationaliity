# Phase 2 baseline odd residual refinement spec

- Spec id: `bz_phase2_baseline_odd_residual_refinement_spec`
- Source post-probe gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_odd_extraction_post_probe_decision_gate.md`
- Source gate id: `bz_phase2_baseline_odd_extraction_post_probe_decision_gate`
- Source extraction rule: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_odd_extraction_rule.md`
- Source rule id: `bz_phase2_baseline_odd_extraction_rule_v1`
- Shared exact window: `n=1..80`
- Active object: `baseline_odd_pair_object_with_constant_residual`

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration for conventions and failure modes. It may not redefine the active odd-pair object or supply hidden identities for it.

## Fixed family ladder

| family | fit window | validation window | coefficients |
| --- | --- | --- | --- |
| `support0_same_index` | `n=1..2` | `n=1..80` | `a, b` |
| `difference_pair` | `n=2..3` | `n=2..80` | `a, b` |
| `support1_lagged_pair` | `n=2..5` | `n=2..80` | `a0, a1, b0, b1` |

## Family details

### `support0_same_index`

- Label: Same-index support-0 constant recombination
- Statement: `r_n = constant_n + a * zeta3_n + b * zeta5_n`
- Goal: Test whether the constant residual collapses under a same-index exact recombination with the retained odd pair.

### `difference_pair`

- Label: First-difference odd-pair recombination
- Statement: `r_n = constant_n + a * (zeta3_n - zeta3_{n-1}) + b * (zeta5_n - zeta5_{n-1})`
- Goal: Test whether the constant residual is better described against first differences of the retained odd pair.

### `support1_lagged_pair`

- Label: Lag-1 odd-pair support recombination
- Statement: `r_n = constant_n + a0 * zeta3_n + a1 * zeta3_{n-1} + b0 * zeta5_n + b1 * zeta5_{n-1}`
- Goal: Test whether one lag of odd-pair support is enough to reclassify the constant residual.

## Non-goals

- Do not fit any bridge-side object in this refinement ladder.
- Do not enlarge to support-2 or n-dependent families in this tranche.
- Do not claim a baseline P_n extraction from these families alone.

## Recommendation

Run the bounded odd-pair residual-refinement probe next and let its exact full-window verdict choose between a promoted v2 odd extraction branch and a hard-wall decision gate.
