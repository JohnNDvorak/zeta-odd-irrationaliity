---
title: Sym4 Generalized Polynomial Matrix Lead
category: conclusion
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup__20260416_123223.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_parity_support_note.md
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

- Homogeneous `(1, 2)` stayed rank-deficient at good primes, with corrected nullity `150`.
- Homogeneous `(1, 3)` stayed rank-deficient at good primes, with corrected nullity `360`.
- Affine `(1, 2)` stayed rank-deficient at good primes, with corrected nullity `150`.
- Target reductions at primes `1009` and `1459` were skipped as denominator-singular.
- The affine target fingerprint has a stable free-column pattern: degree-2 matrix coefficients `M[2,0,i,j]` with target index `i=0..14` and source index `j=5..14`.
- The target sequence is parity-sparse: coordinate `0` is nonzero for all `n`, while coordinates `1..14` are nonzero exactly on odd `n`.

## Correction Note

The smaller nullity ranges in the first follow-up snapshot were caused by an incorrect finite-field `DomainMatrix` constructor path. The corrected code uses `DomainMatrix.from_list(rows, GF(p))` and direct nullspace-row verification.

## Next Action

Classify the stable `150`-dimensional affine target nullspace before trying another family: test whether the parity-sparse degree-2 matrix-block freedom is gauge/coordinate slack or contains a smaller exact recurrence-bearing subspace.
