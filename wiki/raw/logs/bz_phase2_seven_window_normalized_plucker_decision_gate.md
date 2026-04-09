# Phase 2 seven-window normalized Plucker decision gate

- Gate id: `bz_phase2_seven_window_normalized_plucker_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_seven_window_normalized_plucker_matrix_recurrence_screen.md`
- Source probe id: `bz_phase2_seven_window_normalized_plucker_probe`
- Shared exact window: `n=1..74`
- Outcome: `hard_wall_seven_window_plucker_low_order_matrix_ladder_exhausted`

| side | recurrence order | verdict | witness prime |
| --- | --- | --- | --- |
| `source` | `1` | `inconsistent_mod_prime` | `1013` |
| `target` | `1` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `inconsistent_mod_prime` | `1013` |
| `target` | `2` | `inconsistent_mod_prime` | `1447` |

## Rationale

The overdetermined low-order constant matrix ladder is now closed on the seven-window object, and order 3 is already underdetermined.

## Next step

Keep the seven-window object only if there is a genuinely different nonlocal family to test. Otherwise pivot again to a different wider-window nonlinear invariant.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared seven-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Pivot options

- `different_nonlocal_family_on_seven_window_plucker`
- `different_wider_window_nonlinear_object`
