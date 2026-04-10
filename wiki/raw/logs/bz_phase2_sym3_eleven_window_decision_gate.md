# Phase 2 Sym^3-lifted eleven-window decision gate

- Gate id: `bz_phase2_sym3_eleven_window_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_sym3_eleven_window_matrix_recurrence_screen.md`
- Source probe id: `bz_phase2_sym3_eleven_window_probe`
- Shared exact window: `n=1..70`
- Outcome: `hard_wall_sym3_eleven_window_low_order_matrix_ladder_exhausted`

| side | recurrence order | verdict | witness prime |
| --- | --- | --- | --- |
| `source` | `1` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `inconsistent_mod_prime` | `1447` |
| `source` | `3` | `inconsistent_mod_prime` | `1009` |
| `target` | `3` | `inconsistent_mod_prime` | `1447` |
| `source` | `4` | `inconsistent_mod_prime` | `1009` |
| `target` | `4` | `inconsistent_mod_prime` | `1447` |
| `source` | `5` | `inconsistent_mod_prime` | `1009` |
| `target` | `5` | `inconsistent_mod_prime` | `1447` |
| `source` | `6` | `inconsistent_mod_prime` | `1009` |
| `target` | `6` | `inconsistent_mod_prime` | `1447` |

## Rationale

The overdetermined homogeneous matrix screen is closed through order 6 on the Sym^3-lifted eleven-window object, and order 7 is already underdetermined.

## Next step

Keep the Sym^3-lifted eleven-window object only if there is a genuinely different nonlocal family to test. Otherwise pivot to a different higher nonlinear invariant family.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^3-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Pivot options

- `different_nonlocal_family_on_sym3_eleven_window_lift`
- `different_higher_schur_or_nonlinear_invariant_family`
