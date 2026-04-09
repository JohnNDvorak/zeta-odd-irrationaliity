# Phase 2 symmetric-dual to baseline-dual six-chart screen

- Object class: `six_term_window_chart_profile`
- Source family: `totally_symmetric_dual_f7_packet`
- Target family: `baseline_dual_f7_packet`
- Shared exact window: `n=1..75`

## Definition

For each six-term packet window `(v_n, ..., v_{n+5})`, use the first three packet vectors as a local basis and express
the next three packet vectors in that basis. This yields a 9-dimensional exact chart vector per window.

## Screen result

- Singular windows:
  - source: none
  - target: none
- Direct chart equality fails on the full shared window.

## Bounded family ladder

| family | fit block | first mismatch after fit |
| --- | --- | --- |
| `constant_chart9_map` | `n=1..9` | `10` |
| `difference_chart9_map` | `n=2..10` | `11` |
| `support1_chart9_map` | `n=2..19` | `20` |
| `support2_chart9_map` | `n=3..29` | `30` |
| `support3_chart9_map` | `n=4..39` | `40` |

## Interpretation

This object is stronger than the five-term chart object: the mismatch frontier moves from
`7, 8, 14, 21, 28, 35` to `10, 11, 20, 30, 40`.

However, the pattern is still interpolation-only. Each richer support family fails immediately after its exact fit block.
So the six-term chart object does not justify another full support-depth escalation on the same family.

## Recommendation

Do not codify a larger linear support ladder on the six-term chart object.

The next object class should be genuinely nonlinear and subspace-invariant, for example a normalized Plucker-coordinate
window invariant, rather than a larger chart/support interpolation family.
