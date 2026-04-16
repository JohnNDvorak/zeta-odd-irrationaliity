---
title: Sym4 Generalized Polynomial Matrix Lead
category: conclusion
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md
last_updated: '2026-04-16'
---

Banked lead: the non-monic polynomial matrix recurrence screen on the [[sym4-sixteen-window-object]] did not close three target-side order-1 cases, and a bounded independent prime follow-up found persistent modular nullity rather than a full-column-rank obstruction.

## Open Cases

- Homogeneous target-side `(order, degree) = (1, 2)`, with `960` equations and `678` unknowns.
- Homogeneous target-side `(order, degree) = (1, 3)`, with `960` equations and `904` unknowns.
- Affine target-side `(order, degree) = (1, 2)`, with `960` equations and `723` unknowns.

## What This Means

This is not a proof of a recurrence. It is a precise exact-follow-up target: the full-rank modular obstruction did not certify these cases at the known target witness primes, and the bounded follow-up also found rank deficiency at every good prime tested.

Follow-up details:

- Homogeneous `(1, 2)` stayed rank-deficient at good primes, with nullity range `11..37`.
- Homogeneous `(1, 3)` stayed rank-deficient at good primes, with nullity range `41..143`.
- Affine `(1, 2)` stayed rank-deficient at good primes, with nullity range `10..11`.
- Target reductions at primes `1009` and `1459` were skipped as denominator-singular.

## Next Action

Run exact nullspace extraction/certification on these three target-side cases, starting with affine `(order, degree) = (1, 2)` because its modular nullity is smallest and most stable.
