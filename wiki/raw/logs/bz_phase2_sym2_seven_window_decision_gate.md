# Phase 2 Sym^2-lifted seven-window decision gate

- Gate id: `bz_phase2_sym2_seven_window_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_sym2_seven_window_matrix_recurrence_screen.md`
- Source probe id: `bz_phase2_sym2_seven_window_probe`
- Shared exact window: `n=1..74`
- Outcome: `hard_wall_sym2_seven_window_low_order_matrix_ladder_exhausted`

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
| `source` | `7` | `inconsistent_mod_prime` | `1009` |
| `target` | `7` | `inconsistent_mod_prime` | `1447` |
| `source` | `8` | `inconsistent_mod_prime` | `1009` |
| `target` | `8` | `inconsistent_mod_prime` | `1447` |
| `source` | `9` | `inconsistent_mod_prime` | `1009` |
| `target` | `9` | `inconsistent_mod_prime` | `1447` |
| `source` | `10` | `inconsistent_mod_prime` | `1009` |
| `target` | `10` | `inconsistent_mod_prime` | `1447` |

## Rationale

The overdetermined low-order constant matrix ladder is now closed on the lifted object through order 10, and order 11 is already underdetermined.

## Next step

Keep the Sym^2-lifted object only if there is a genuinely different nonlocal family to test. Otherwise pivot again to a different beyond-Plucker invariant family.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Pivot options

- `different_nonlocal_family_on_sym2_lift`
- `different_beyond_plucker_invariant_family`
