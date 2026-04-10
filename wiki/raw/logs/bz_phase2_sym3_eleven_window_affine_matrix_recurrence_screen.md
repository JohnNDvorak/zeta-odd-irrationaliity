# Phase 2 Sym^3-lifted eleven-window affine matrix recurrence screen

- Screen id: `bz_phase2_sym3_eleven_window_affine_matrix_recurrence_screen`
- Source probe id: `bz_phase2_sym3_eleven_window_probe`
- Shared exact window: `n=1..70`
- Overall verdict: `low_order_affine_matrix_recurrence_exhausted_through_order_6`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `10` | `690` | `110` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `10` | `690` | `110` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `10` | `680` | `210` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `10` | `680` | `210` | `inconsistent_mod_prime` | `1447` |
| `source` | `3` | `10` | `670` | `310` | `inconsistent_mod_prime` | `1009` |
| `target` | `3` | `10` | `670` | `310` | `inconsistent_mod_prime` | `1447` |
| `source` | `4` | `10` | `660` | `410` | `inconsistent_mod_prime` | `1009` |
| `target` | `4` | `10` | `660` | `410` | `inconsistent_mod_prime` | `1447` |
| `source` | `5` | `10` | `650` | `510` | `inconsistent_mod_prime` | `1009` |
| `target` | `5` | `10` | `650` | `510` | `inconsistent_mod_prime` | `1447` |
| `source` | `6` | `10` | `640` | `610` | `inconsistent_mod_prime` | `1009` |
| `target` | `6` | `10` | `640` | `610` | `inconsistent_mod_prime` | `1447` |

## Interpretation

This screen tests affine matrix-valued recurrences on the Sym^3-lifted eleven-window normalized maximal-minor sequence, for recurrence orders `1` through `6`, separately on the source and target side. Order `7` is the first underdetermined case on this lifted object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^3-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing affine matrix recurrence order mechanically. Order 7 is the first underdetermined case on this lifted object, so further escalation would cross from obstruction screening into interpolation territory.
