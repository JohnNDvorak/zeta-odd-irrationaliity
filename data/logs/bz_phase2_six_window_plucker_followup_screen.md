# Phase 2 six-window Plucker follow-up screen

- Base invariant family: `normalized_plucker_window_invariant`
- Source family: `totally_symmetric_dual_f7_packet`
- Target family: `baseline_dual_f7_packet`
- Follow-up window model: `six_term_window`
- Shared exact window: `n=1..75`

## 1. Full six-window normalized Plucker object

Use the normalized `Gr(3,6)` Plucker coordinate vector on each six-term packet window
`(v_n, ..., v_{n+5})`, with pivot minor `(1,2,3)` omitted after normalization.

This produces a `19`-coordinate nonlinear window invariant.

Cheap exact ladder:

| family | first mismatch after fit |
| --- | --- |
| `constant_six_plucker_map` | `20` |
| `difference_six_plucker_map` | `21` |

This is a real improvement over the five-term normalized Plucker object, whose cheap ladder began at
`10, 11`.

However, the first lagged family is not merely a mismatch. On the initial support-1 fit block, the exact
`722 x 722` system is singular, so the old support ladder is not even well-posed in the same form on this
object.

## 2. Fixed-anchor six-window projective quotient

Use the stable nonzero six-window Plucker coordinate `124` as a global anchor and divide the remaining
eighteen non-pivot coordinates by that anchor.

Cheap exact ladder:

| family | first mismatch after fit |
| --- | --- |
| `constant_six_projective_quotient_map` | `19` |
| `difference_six_projective_quotient_map` | `20` |

So the projective quotient is weaker than the full six-window normalized Plucker object. It removes one
coordinate but does not improve the transfer frontier.

## Interpretation

The wider-window nonlinear move is real: the full six-window normalized Plucker object improves the cheap
frontier from `10, 11` to `20, 21`.

But the quotient continuation does not help. The fixed-anchor projective quotient drops back to `19, 20`,
and the direct support-1 ladder on the full six-window object becomes singular rather than predictive.

This is a different wall from the earlier interpolation-only pattern:

- five-term chart / Plucker objects: richer support depth was available but interpolation-only
- six-term normalized Plucker object: cheap frontier improves, but the first richer support family is
  ill-posed on the initial fit block

## Recommendation

Do not spend more time on six-window Plucker quotients.

The promising object is the full six-window normalized Plucker invariant itself. If we stay in this wider
window family, the next step should be a different recurrence-level family on that object, not another
projective or cross-ratio quotient.
