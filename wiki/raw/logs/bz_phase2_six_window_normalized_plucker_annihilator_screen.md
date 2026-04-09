# Phase 2 six-window normalized Plucker annihilator screen

- Screen id: `bz_phase2_six_window_normalized_plucker_annihilator_screen`
- Source probe id: `bz_phase2_six_window_normalized_plucker_probe`
- Shared exact window: `n=1..75`
- Overall verdict: `short_order_local_annihilator_family_exhausted_up_to_order_6`

| side | relation length | window count | first inconsistent index | first nonunique index | verdict |
| --- | --- | --- | --- | --- | --- |
| `source` | `4` | `72` | `1` | `None` | `screen_fails` |
| `target` | `4` | `72` | `1` | `None` | `screen_fails` |
| `source` | `5` | `71` | `1` | `None` | `screen_fails` |
| `target` | `5` | `71` | `1` | `None` | `screen_fails` |
| `source` | `6` | `70` | `1` | `None` | `screen_fails` |
| `target` | `6` | `70` | `1` | `None` | `screen_fails` |

## Interpretation

This screen tests short-order local annihilator families directly on the six-window normalized Plucker sequence itself, not on transfer-map residuals.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared six-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep enlarging short local annihilator order on the six-window normalized Plucker object without a new structural reason.
