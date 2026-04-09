# Phase 2 seven-window normalized Plucker matrix recurrence screen

- Screen id: `bz_phase2_seven_window_normalized_plucker_matrix_recurrence_screen`
- Source probe id: `bz_phase2_seven_window_normalized_plucker_probe`
- Shared exact window: `n=1..74`
- Overall verdict: `low_order_matrix_recurrence_exhausted_through_order_2`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `34` | `2482` | `1156` | `inconsistent_mod_prime` | `1013` |
| `target` | `1` | `34` | `2482` | `1156` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `34` | `2448` | `2312` | `inconsistent_mod_prime` | `1013` |
| `target` | `2` | `34` | `2448` | `2312` | `inconsistent_mod_prime` | `1447` |

## Interpretation

This screen tests constant matrix-valued recurrences on the seven-window normalized Plucker sequence, for recurrence orders `1` and `2`, separately on the source and target side. Inconsistency is certified by finite-field obstruction when found. Order `3` is the first underdetermined case on this object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared seven-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing matrix recurrence order mechanically. Order 3 is the first underdetermined case on this object, so further escalation would cross from obstruction screening into interpolation territory.
