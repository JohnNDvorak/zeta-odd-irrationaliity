# Phase 2 eight-window normalized Plucker matrix recurrence screen

- Screen id: `bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen`
- Source probe id: `bz_phase2_eight_window_normalized_plucker_probe`
- Shared exact window: `n=1..73`
- Overall verdict: `order1_matrix_recurrence_exhausted`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `55` | `3960` | `3025` | `inconsistent_mod_prime` | `1013` |
| `target` | `1` | `55` | `3960` | `3025` | `inconsistent_mod_prime` | `1447` |

## Interpretation

This screen tests the last overdetermined constant matrix-valued recurrence on the eight-window normalized Plucker sequence, separately on the source and target side. Order `2` is already underdetermined on this object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared eight-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing matrix recurrence order mechanically. Order 2 is already underdetermined on this object, so the next move must be a different nonlocal family or a different wider invariant.
