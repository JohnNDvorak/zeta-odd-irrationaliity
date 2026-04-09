# Phase 2 symmetric source packet compression probe

- Probe id: `bz_phase2_symmetric_source_packet_compression_probe`
- Source gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_source_packet_post_probe_decision_gate.md`
- Source gate id: `bz_phase2_symmetric_source_packet_post_probe_decision_gate`
- Shared exact window: `n=1..80`
- Overall verdict: `pairwise_low_complexity_symmetric_source_packet_compression_exhausted`

## Route results

### `retain_scaled_q_scaled_p_residual_scaled_phat`

- Retained pair: `(scaled Q_n, scaled P_n)`
- Residual channel: `scaled Phat_n`
- Route verdict: `hard_wall_low_complexity_scaled_phat_n_residual_exhausted`
- Note: All fixed low-complexity families fail after their fit windows.

| family | verdict | first mismatch index | zero count | residual hash |
| --- | --- | --- | --- | --- |
| `support0_same_index` | `fails_after_fit_window` | `3` | `2` | `cf98bea0fce95e032026c7193ae1db82038731be52de190d8a2a8235a420a4b1` |
| `difference_pair` | `fails_after_fit_window` | `4` | `2` | `c6b6b41d4eb89ada7c4ba4b8c791da2dd279e897477bd8e23a7206587c42aadc` |
| `support1_lagged_pair` | `fails_after_fit_window` | `6` | `4` | `11878f1529a60b52c1a217f3c1eaaa6d1ef34252d136579999e80a29be1954e8` |

### `retain_scaled_q_scaled_phat_residual_scaled_p`

- Retained pair: `(scaled Q_n, scaled Phat_n)`
- Residual channel: `scaled P_n`
- Route verdict: `hard_wall_low_complexity_scaled_p_n_residual_exhausted`
- Note: All fixed low-complexity families fail after their fit windows.

| family | verdict | first mismatch index | zero count | residual hash |
| --- | --- | --- | --- | --- |
| `support0_same_index` | `fails_after_fit_window` | `3` | `2` | `a7b5157dfe6c9a85a67824032e78f471f40a7399a990b51848c3b78971cfe133` |
| `difference_pair` | `fails_after_fit_window` | `4` | `2` | `8ece84db2c42e263891d22f80d84616c69de21398d839e148d95fca21c1a4298` |
| `support1_lagged_pair` | `fails_after_fit_window` | `6` | `4` | `de3444c4b7e035a9c721980e1eae4067ee78805e18de5404c977b683c0aaf265` |

### `retain_scaled_p_scaled_phat_residual_scaled_q`

- Retained pair: `(scaled P_n, scaled Phat_n)`
- Residual channel: `scaled Q_n`
- Route verdict: `hard_wall_low_complexity_scaled_q_n_residual_exhausted`
- Note: All fixed low-complexity families fail after their fit windows.

| family | verdict | first mismatch index | zero count | residual hash |
| --- | --- | --- | --- | --- |
| `support0_same_index` | `fails_after_fit_window` | `3` | `2` | `ef19fa5f4ba4107e9832ff7166503c237c9271af15d7f757080e66745f7dbc37` |
| `difference_pair` | `fails_after_fit_window` | `4` | `2` | `3a705946bfdcf3080dd228a11245aa5aaac003acbb9ab115350399030a41b367` |
| `support1_lagged_pair` | `fails_after_fit_window` | `6` | `4` | `e0885e69e7e7ddf9b658e08b70b511a418bb00f38909c88a50c1f86d4eacc53a` |

## Source boundary

The symmetric source family remains a source-backed anchor, not a hidden claim of baseline equivalence.

## Recommendation

Stop and ask for the next pivot.
