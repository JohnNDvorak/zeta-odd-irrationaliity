# Phase 2 baseline full-packet compression probe

- Probe id: `bz_phase2_baseline_full_packet_compression_probe`
- Source gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_full_packet_post_probe_decision_gate.md`
- Source gate id: `bz_phase2_baseline_full_packet_post_probe_decision_gate`
- Shared exact window: `n=1..80`
- Overall verdict: `pairwise_low_complexity_packet_compression_exhausted`

## Route results

### `retain_constant_zeta5_residual_zeta3`

- Retained pair: `(constant, zeta(5))`
- Residual channel: `zeta(3)`
- Route verdict: `hard_wall_low_complexity_baseline_refinement_exhausted`
- Source: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_residual_refinement_decision_gate.md`
- Note: Previously closed by the constant/zeta(5) residual-refinement hard-wall gate.

### `retain_zeta5_zeta3_residual_constant`

- Retained pair: `(zeta(5), zeta(3))`
- Residual channel: `constant`
- Route verdict: `hard_wall_low_complexity_odd_refinement_exhausted`
- Source: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_odd_residual_refinement_decision_gate.md`
- Note: Previously closed by the odd-pair residual-refinement hard-wall gate.

### `retain_constant_zeta3_residual_zeta5`

- Retained pair: `(constant, zeta(3))`
- Residual channel: `zeta(5)`
- Route verdict: `hard_wall_low_complexity_zeta5_residual_exhausted`
- Source: `computed_inline_from_full_packet`
- Note: Newly computed zeta(5)-residual route; all fixed low-complexity families fail after their fit windows.

| family | verdict | first mismatch index | zero count | residual hash |
| --- | --- | --- | --- | --- |
| `support0_same_index` | `fails_after_fit_window` | `3` | `2` | `dbbb8cf94426761ec7e713b4e3d9e38aa198219e9e5283ac9c227d0c8969aaf5` |
| `difference_pair` | `fails_after_fit_window` | `4` | `2` | `d06e3f6fd8a2109d253ebcb7f6bc880825defa7ef5aab60824cb0e7809c6bab2` |
| `support1_lagged_pair` | `fails_after_fit_window` | `6` | `4` | `c79f3f1f9a3ee985ebf04d31ecd4f80fc4d6af85edd1ae3eeb03fb0bbea3c364` |

## Bridge boundary

The Zudilin 2002 bridge stack remains calibration-only throughout packet compression.

## Recommendation

Stop autonomous execution and ask the user for the next pivot.
