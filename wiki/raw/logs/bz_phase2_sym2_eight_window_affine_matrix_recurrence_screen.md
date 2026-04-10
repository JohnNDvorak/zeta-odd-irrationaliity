# Phase 2 Sym^2-lifted eight-window affine matrix recurrence screen

- Screen id: `bz_phase2_sym2_eight_window_affine_matrix_recurrence_screen`
- Source probe id: `bz_phase2_sym2_eight_window_probe`
- Shared exact window: `n=1..73`
- Overall verdict: `low_order_affine_matrix_recurrence_exhausted_through_order_2`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `27` | `1944` | `756` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `27` | `1944` | `756` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `27` | `1917` | `1485` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `27` | `1917` | `1485` | `inconsistent_mod_prime` | `1447` |

## Interpretation

This screen tests affine matrix-valued recurrences on the Sym^2-lifted eight-window normalized maximal-minor sequence, for recurrence orders `1` and `2`, separately on the source and target side. Order `3` is the first underdetermined case on this lifted object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing affine matrix recurrence order mechanically. Order 3 is the first underdetermined case on this lifted object, so further escalation would cross from obstruction screening into interpolation territory.
