# Phase 2 Sym^4-lifted sixteen-window generalized polynomial matrix recurrence screen

- Screen id: `bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen`
- Source probe id: `bz_phase2_sym4_sixteen_window_probe`
- Shared exact window: `n=1..65`
- Overall verdict: `sym4_sixteen_window_generalized_polynomial_matrix_recurrence_requires_exact_followup`

| family | side | recurrence order | polynomial degree | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `homogeneous` | `source` | `1` | `0` | `15` | `960` | `226` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `0` | `15` | `960` | `226` | `full_column_rank_mod_prime` | `1451` |
| `homogeneous` | `source` | `1` | `1` | `15` | `960` | `452` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `1` | `15` | `960` | `452` | `full_column_rank_mod_prime` | `1451` |
| `homogeneous` | `source` | `1` | `2` | `15` | `960` | `678` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `2` | `15` | `960` | `678` | `no_full_rank_obstruction_found` | `None` |
| `homogeneous` | `source` | `1` | `3` | `15` | `960` | `904` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `1` | `3` | `15` | `960` | `904` | `no_full_rank_obstruction_found` | `None` |
| `homogeneous` | `source` | `2` | `0` | `15` | `945` | `451` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `2` | `0` | `15` | `945` | `451` | `full_column_rank_mod_prime` | `1451` |
| `homogeneous` | `source` | `2` | `1` | `15` | `945` | `902` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `2` | `1` | `15` | `945` | `902` | `full_column_rank_mod_prime` | `1451` |
| `homogeneous` | `source` | `3` | `0` | `15` | `930` | `676` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `3` | `0` | `15` | `930` | `676` | `full_column_rank_mod_prime` | `1451` |
| `homogeneous` | `source` | `4` | `0` | `15` | `915` | `901` | `full_column_rank_mod_prime` | `1009` |
| `homogeneous` | `target` | `4` | `0` | `15` | `915` | `901` | `full_column_rank_mod_prime` | `1451` |
| `affine` | `source` | `1` | `0` | `15` | `960` | `241` | `full_column_rank_mod_prime` | `1009` |
| `affine` | `target` | `1` | `0` | `15` | `960` | `241` | `full_column_rank_mod_prime` | `1451` |
| `affine` | `source` | `1` | `1` | `15` | `960` | `482` | `full_column_rank_mod_prime` | `1009` |
| `affine` | `target` | `1` | `1` | `15` | `960` | `482` | `full_column_rank_mod_prime` | `1451` |
| `affine` | `source` | `1` | `2` | `15` | `960` | `723` | `full_column_rank_mod_prime` | `1009` |
| `affine` | `target` | `1` | `2` | `15` | `960` | `723` | `no_full_rank_obstruction_found` | `None` |
| `affine` | `source` | `2` | `0` | `15` | `945` | `466` | `full_column_rank_mod_prime` | `1009` |
| `affine` | `target` | `2` | `0` | `15` | `945` | `466` | `full_column_rank_mod_prime` | `1451` |
| `affine` | `source` | `2` | `1` | `15` | `945` | `932` | `full_column_rank_mod_prime` | `1009` |
| `affine` | `target` | `2` | `1` | `15` | `945` | `932` | `full_column_rank_mod_prime` | `1451` |
| `affine` | `source` | `3` | `0` | `15` | `930` | `691` | `full_column_rank_mod_prime` | `1009` |
| `affine` | `target` | `3` | `0` | `15` | `930` | `691` | `full_column_rank_mod_prime` | `1451` |

## Interpretation

This screen tests non-monic matrix-valued recurrences whose coefficients are low-degree polynomials in the target index `n`. Unlike the monic polynomial matrix screen, this family also allows a scalar polynomial coefficient on the target vector. It is closer to the usual P-recursive shape while still staying within strict overdetermined cases.

## Cases

- Homogeneous: `(order, degree) = (1, 0)`, `(1, 1)`, `(1, 2)`, `(1, 3)`, `(2, 0)`, `(2, 1)`, `(3, 0)`, and `(4, 0)`.
- Affine: `(order, degree) = (1, 0)`, `(1, 1)`, `(1, 2)`, `(2, 0)`, `(2, 1)`, and `(3, 0)`.

## Boundary

- Homogeneous `(order, degree) = (1, 4)` would have `1130` unknowns against `960` equations.
- Homogeneous `(order, degree) = (2, 2)` would have `1353` unknowns against `945` equations.
- Homogeneous `(order, degree) = (3, 1)` would have `1352` unknowns against `930` equations.
- Affine `(order, degree) = (1, 3)` would have `964` unknowns against `960` equations.
- Affine `(order, degree) = (2, 2)` would have `1398` unknowns against `945` equations.
- Affine `(order, degree) = (3, 1)` would have `1382` unknowns against `930` equations.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

A full-rank modular obstruction was not found for at least one generalized polynomial matrix case; exact follow-up is required before banking this family as exhausted.
