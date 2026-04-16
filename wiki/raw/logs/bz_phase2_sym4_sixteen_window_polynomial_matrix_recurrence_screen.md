# Phase 2 Sym^4-lifted sixteen-window polynomial matrix recurrence screen

- Screen id: `bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen`
- Source probe id: `bz_phase2_sym4_sixteen_window_probe`
- Shared exact window: `n=1..65`
- Overall verdict: `low_degree_polynomial_matrix_recurrence_exhausted_over_overdetermined_range`

| family | side | recurrence order | polynomial degree | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `homogeneous` | `source` | `1` | `1` | `15` | `960` | `450` | `inconsistent_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `1` | `15` | `960` | `450` | `inconsistent_mod_prime` | `1451` |
| `homogeneous` | `source` | `1` | `2` | `15` | `960` | `675` | `inconsistent_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `2` | `15` | `960` | `675` | `inconsistent_mod_prime` | `1451` |
| `homogeneous` | `source` | `1` | `3` | `15` | `960` | `900` | `inconsistent_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `3` | `15` | `960` | `900` | `inconsistent_mod_prime` | `1451` |
| `homogeneous` | `source` | `2` | `1` | `15` | `945` | `900` | `inconsistent_mod_prime` | `1009` |
| `homogeneous` | `target` | `2` | `1` | `15` | `945` | `900` | `inconsistent_mod_prime` | `1451` |
| `affine` | `source` | `1` | `1` | `15` | `960` | `480` | `inconsistent_mod_prime` | `1009` |
| `affine` | `target` | `1` | `1` | `15` | `960` | `480` | `inconsistent_mod_prime` | `1451` |
| `affine` | `source` | `1` | `2` | `15` | `960` | `720` | `inconsistent_mod_prime` | `1009` |
| `affine` | `target` | `1` | `2` | `15` | `960` | `720` | `inconsistent_mod_prime` | `1451` |
| `affine` | `source` | `2` | `1` | `15` | `945` | `930` | `inconsistent_mod_prime` | `1009` |
| `affine` | `target` | `2` | `1` | `15` | `945` | `930` | `inconsistent_mod_prime` | `1451` |

## Interpretation

This screen tests matrix-valued recurrences whose coefficients are low-degree polynomials in the target index `n`, on the Sym^4-lifted sixteen-window normalized maximal-minor sequence. It only includes cases that remain strict overdetermined after the constant-coefficient matrix ladders have closed.

## Cases

- Homogeneous: `(order, degree) = (1, 1)`, `(1, 2)`, `(1, 3)`, and `(2, 1)`.
- Affine: `(order, degree) = (1, 1)`, `(1, 2)`, and `(2, 1)`.

## Boundary

- Homogeneous `(order, degree) = (1, 4)` would have `1125` unknowns against `960` equations.
- Homogeneous `(order, degree) = (2, 2)` would have `1350` unknowns against `945` equations.
- Affine `(order, degree) = (1, 3)` would have `960` unknowns against `960` equations.
- Affine `(order, degree) = (2, 2)` would have `1395` unknowns against `945` equations.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not escalate polynomial degree or recurrence order mechanically. The remaining polynomial matrix cases are no longer strict overdetermined obstruction screens.
