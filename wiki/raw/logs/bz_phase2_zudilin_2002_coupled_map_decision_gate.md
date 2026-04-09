# Phase 2 Zudilin 2002 coupled-map decision gate

- Gate id: `bz_phase2_zudilin_2002_coupled_map_decision_gate`
- Shared exact window: `n=1..7`

| layer | verdict | implication |
| --- | --- | --- |
| `one_channel_polynomial_maps` | `closed` | Scalar, affine-in-n, and quadratic-in-n one-channel normalization families all fail exactly on the shared window. |
| `constant_coupled_linear_map` | `closed` | A constant rational 2x2 transformation fitted from n=1,2 does not carry the bridge pair to the baseline pair on the full shared window. |

## Overall verdict

The bounded constant-form ansatz layer is now closed. Both the one-channel polynomial-rescaling line and the simplest coupled constant-matrix line fail on the shared window.

## Recommendation

Do not keep enlarging the ansatz mechanically. The next bounded move should either test one structured n-dependent two-channel map family or pivot to a different paired object / projection target.

## Non-claims

- This does not rule out all coupled transformations.
- This does not prove the baseline pair and bridge pair are unrelated in every stronger sense.
- This only closes the bounded constant-form ansatz layer tested so far.
