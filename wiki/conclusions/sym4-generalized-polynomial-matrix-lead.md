---
title: Sym4 Generalized Polynomial Matrix Lead
category: conclusion
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
last_updated: '2026-04-16'
---

Banked lead: the non-monic polynomial matrix recurrence screen on the [[sym4-sixteen-window-object]] did not close three target-side order-1 cases at the known witness primes.

## Open Cases

- Homogeneous target-side `(order, degree) = (1, 2)`, with `960` equations and `678` unknowns.
- Homogeneous target-side `(order, degree) = (1, 3)`, with `960` equations and `904` unknowns.
- Affine target-side `(order, degree) = (1, 2)`, with `960` equations and `723` unknowns.

## What This Means

This is not a proof of a recurrence. It is a precise exact-follow-up target: the full-rank modular obstruction did not certify these cases at the known target witness primes, while the surrounding source-side and lower-order target-side cases did close.

## Next Action

Run exact or independently certified modular nullspace follow-up on these three target-side cases before trying another family.
