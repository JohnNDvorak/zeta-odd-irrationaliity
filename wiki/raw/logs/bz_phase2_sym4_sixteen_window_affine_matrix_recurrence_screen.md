# Phase 2 Sym^4-lifted sixteen-window affine matrix recurrence screen

- Screen id: `bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen`
- Source probe id: `bz_phase2_sym4_sixteen_window_probe`
- Shared exact window: `n=1..65`
- Overall verdict: `low_order_affine_matrix_recurrence_exhausted_through_order_3`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `15` | `960` | `240` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `15` | `960` | `240` | `inconsistent_mod_prime` | `1451` |
| `source` | `2` | `15` | `945` | `465` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `15` | `945` | `465` | `inconsistent_mod_prime` | `1451` |
| `source` | `3` | `15` | `930` | `690` | `inconsistent_mod_prime` | `1009` |
| `target` | `3` | `15` | `930` | `690` | `inconsistent_mod_prime` | `1451` |

## Interpretation

This screen tests affine matrix-valued recurrences on the Sym^4-lifted sixteen-window normalized maximal-minor sequence, for recurrence orders `1` through `3`, separately on the source and target side. Order `4` is already non-overdetermined on this lifted object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing affine matrix recurrence order mechanically. Order 4 is already non-overdetermined on this lifted object, so further escalation would cross from obstruction screening into interpolation territory.
