# Phase 2 Zudilin 2002 normalization decision gate

- Gate id: `bz_phase2_zudilin_2002_normalization_decision_gate`
- Shared exact window: `n=1..7`

| family | verdict | mismatch indices | implication |
| --- | --- | --- | --- |
| `scalar` | `simple_scalar_map_fails` | `2,3,4,5,6,7` | The channels are not related by a single exact rational rescaling on the shared window. |
| `affine_in_n` | `affine_scalar_map_fails` | `3,4,5,6,7` | The channels are not related by an exact affine-in-n rescaling on the shared window. |
| `quadratic_in_n` | `quadratic_scalar_map_fails` | `4,5,6,7` | The channels are not related by an exact quadratic-in-n rescaling on the shared window. |

## Overall verdict

Three bounded polynomial normalization families now fail exactly on the shared n=1..7 window. That is enough evidence to stop the polynomial-rescaling subline instead of extending it mechanically.

## Recommendation

Switch away from scalar/affine/quadratic normalization maps and move to a different bridge-comparison ansatz, such as a companion-channel-aware transformation or a structurally different projection target.

## Non-claims

- This does not rule out all possible normalization maps.
- This does not prove the baseline and Zudilin bridge channels are unrelated in every stronger sense.
- This only closes the bounded polynomial-rescaling subline tested so far.
