# Phase 2 six-window normalized Plucker matrix recurrence screen

- Screen id: `bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen`
- Source probe id: `bz_phase2_six_window_normalized_plucker_probe`
- Shared exact window: `n=1..75`
- Overall verdict: `low_order_matrix_recurrence_exhausted_through_order_3`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `19` | `1406` | `361` | `inconsistent_mod_prime` | `1013` |
| `target` | `1` | `19` | `1406` | `361` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `19` | `1387` | `722` | `inconsistent_mod_prime` | `1013` |
| `target` | `2` | `19` | `1387` | `722` | `inconsistent_mod_prime` | `1447` |
| `source` | `3` | `19` | `1368` | `1083` | `inconsistent_mod_prime` | `1013` |
| `target` | `3` | `19` | `1368` | `1083` | `inconsistent_mod_prime` | `1447` |

## Interpretation

This screen tests constant matrix-valued recurrences on the six-window normalized Plucker sequence, for recurrence orders `1`, `2`, and `3`, separately on the source and target side. Inconsistency is certified by finite-field obstruction when found.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared six-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing matrix recurrence order mechanically. Order 4 is the first underdetermined case on this object, so further escalation would cross from obstruction screening into interpolation territory.
