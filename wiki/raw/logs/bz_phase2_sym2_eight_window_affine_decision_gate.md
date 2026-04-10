# Phase 2 Sym^2-lifted eight-window affine decision gate

- Gate id: `bz_phase2_sym2_eight_window_affine_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_sym2_eight_window_affine_matrix_recurrence_screen.md`
- Source probe id: `bz_phase2_sym2_eight_window_probe`
- Shared exact window: `n=1..73`
- Outcome: `hard_wall_sym2_eight_window_low_order_affine_matrix_ladder_exhausted`

| side | recurrence order | verdict | witness prime |
| --- | --- | --- | --- |
| `source` | `1` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `inconsistent_mod_prime` | `1447` |

## Rationale

The overdetermined affine matrix screen is closed through order 2 on the Sym^2-lifted eight-window object, and order 3 is already underdetermined.

## Next step

Do not keep widening affine matrix order mechanically. Move either to a genuinely different nonlocal family on the same object or to a different higher Schur/nonlinear invariant family.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Pivot options

- `different_nonlocal_family_on_sym2_eight_window_lift`
- `different_higher_schur_or_nonlinear_invariant_family`
