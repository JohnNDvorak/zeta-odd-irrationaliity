# Phase 2 eight-window normalized Plucker decision gate

- Gate id: `bz_phase2_eight_window_normalized_plucker_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.md`
- Source probe id: `bz_phase2_eight_window_normalized_plucker_probe`
- Shared exact window: `n=1..73`
- Outcome: `hard_wall_eight_window_plucker_order1_matrix_exhausted`

| side | recurrence order | verdict | witness prime |
| --- | --- | --- | --- |
| `source` | `1` | `inconsistent_mod_prime` | `1013` |
| `target` | `1` | `inconsistent_mod_prime` | `1447` |

## Rationale

The last overdetermined constant matrix screen is already closed on the eight-window object, and order 2 is underdetermined.

## Next step

Keep the eight-window object only if there is a genuinely different nonlocal family to test. Otherwise pivot beyond the current normalized Plucker family.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared eight-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Pivot options

- `different_nonlocal_family_on_eight_window_plucker`
- `different_wider_nonlinear_invariant_family`
