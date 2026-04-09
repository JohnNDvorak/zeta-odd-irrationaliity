# Phase 2 normalized Plucker window invariant screen

- Object class: `normalized_plucker_window_invariant`
- Source family: `totally_symmetric_dual_f7_packet`
- Target family: `baseline_dual_f7_packet`
- Screened window model: `five_term_window`
- Shared exact window: `n=1..76`

## Definition

For each five-term packet window `(v_n, ..., v_{n+4})`, use the first three packet vectors as a basis chart and
compute the normalized Plucker coordinates of the induced `Gr(3,5)` point. Concretely, this is the vector of all
`3x3` minors divided by the pivot minor `(1,2,3)`, with the pivot omitted.

This is a nonlinear, subspace-invariant embedding of the same five-term window geometry that the chart-profile object
tracked in local coordinates.

## Screen result

The normalized Plucker invariant is genuinely stronger than the earlier five-term chart object. The bounded exact ladder
on the shared window gives:

| family | first mismatch after fit |
| --- | --- |
| `constant_plucker_map` | `10` |
| `difference_plucker_map` | `11` |
| `support1_plucker_map` | `20` |
| `support2_plucker_map` | `30` |
| `support3_plucker_map` | `40` |

## Interpretation

This is a real improvement over the earlier five-term chart ladder (`7, 8, 14, 21, 28, 35`).

However, the stronger nonlinear invariant is still interpolation-only. Each richer support family fails immediately
after its exact fit block:

- support `0`: mismatch begins at `d + 1`
- support `1`: mismatch begins at `2d + 2`
- support `2`: mismatch begins at `3d + 3`
- support `3`: mismatch begins at `4d + 4`

with `d = 9` for the normalized `Gr(3,5)` Plucker coordinate vector.

So this object class does not justify a larger support-depth escalation without a new structural idea.

## Recommendation

Treat normalized Plucker invariants as screened and promising but still blocked.

If we stay in this family, the next step would need to be a different kind of invariant on the same Grassmannian data,
for example a projective or cross-ratio style quotient of Plucker coordinates, not another linear support ladder.
