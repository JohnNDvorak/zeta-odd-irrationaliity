# Phase 2 baseline decay audit

| object id | family | kind | source status | exact status | max verified index | proof relevance |
| --- | --- | --- | --- | --- | --- | --- |
| `baseline_bz_qn` | `baseline` | `q_sequence` | `source_backed` | `exact` | `12` | `indirect` |
| `baseline_bz_dual_constant` | `baseline` | `dual_constant_sequence` | `derived_local` | `exact` | `434` | `indirect` |
| `baseline_bz_dual_zeta3` | `baseline` | `dual_zeta3_sequence` | `derived_local` | `exact` | `434` | `indirect` |
| `baseline_bz_dual_zeta5` | `baseline` | `dual_zeta5_sequence` | `derived_local` | `exact` | `80` | `indirect` |
| `baseline_bz_pn` | `baseline` | `p_sequence` | `missing_local` | `missing` | `` | `direct` |
| `baseline_bz_remainder` | `baseline` | `remainder_pipeline` | `missing_local` | `missing` | `` | `direct` |
| `totally_symmetric_qn` | `totally_symmetric` | `q_sequence` | `source_backed` | `exact` | `10` | `indirect` |
| `totally_symmetric_pn` | `totally_symmetric` | `p_sequence` | `source_backed` | `exact` | `14` | `direct` |
| `totally_symmetric_phat` | `totally_symmetric` | `phat_sequence` | `source_backed` | `exact` | `14` | `supporting` |
| `totally_symmetric_remainder_pipeline` | `totally_symmetric` | `remainder_pipeline` | `source_backed` | `mixed` | `14` | `direct` |

## Source-backed decay anchor

- Object id: `bz_totally_symmetric_remainder_pipeline`
- Bridge target family: `baseline`
- Exact indices: `[0, 1, ..., 13, 14]`
- Numeric indices: `[1, 2, ..., 13, 14]`
- Metric `log_abs_scaled_q_over_n`: latest `10.28521347`.
- Metric `log_abs_scaled_remainder_over_n`: latest `1.59962451`.
- Metric `gamma`: latest `0.84447338` (published `0.77795976`).

## Baseline decay gap

- Object id: `baseline_bz_remainder_pipeline`
- Missing prerequisites: `No repo-local baseline P_n formula or recurrence.`, `No repo-local baseline remainder / linear-form fixture.`
- Recommendation: Keep baseline decay work on the readiness bridge until a source-backed baseline P_n or remainder object is available locally.
