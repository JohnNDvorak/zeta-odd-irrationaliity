---
title: Sym4 Sixteen-Window Generalized Polynomial Matrix Followup
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup__20260416_123223.md
last_updated: '2026-04-16'
---

Audit record for the bounded prime follow-up on the three target-side cases left open by the [[sym4-sixteen-window-generalized-polynomial-matrix-screen]].

## Scope

- Object: [[sym4-sixteen-window-object]]
- Side: target
- Cases:
  - homogeneous `(order, degree) = (1, 2)`, with `960` equations and `678` unknowns
  - homogeneous `(order, degree) = (1, 3)`, with `960` equations and `904` unknowns
  - affine `(order, degree) = (1, 2)`, with `960` equations and `723` unknowns
- Tested primes: `1451`, `1009`, `1453`, `1459`, `1471`, `1481`, `1483`, `1487`, `1489`, and `1493`

## Outcome

The bounded prime sweep did not find a full-column-rank obstruction for any of the three cases.

- Homogeneous `(1, 2)` stayed rank-deficient at every good prime tested, with corrected nullity `150`.
- Homogeneous `(1, 3)` stayed rank-deficient at every good prime tested, with corrected nullity `360`.
- Affine `(1, 2)` stayed rank-deficient at every good prime tested, with corrected nullity `150`.
- Primes `1009` and `1459` were skipped because denominator reduction was singular for the target data.

## Correction Note

The first banked follow-up snapshot reported smaller nullity ranges. That was an implementation artifact from constructing finite-field matrices with `DomainMatrix(rows, shape, GF(p))`. The corrected code uses `DomainMatrix.from_list(rows, GF(p))`, which agrees with direct nullspace verification on the affine target fingerprint.

## Interpretation

This is a stronger lead than the original known-witness screen, but still not a recurrence. A full column rank at any good prime would have closed a case; instead, modular nullity persisted across the bounded independent prime set.

The next defensible action is not a blind exact reconstruction of a ten-dimensional space. The corrected nullities are large and stable, so the immediate follow-up is to classify the visible nullspace structure before trying another family.

## Guardrail

Do not describe this as a banked recurrence. It is a banked exact-follow-up target on the strongest repo-native quartic invariant.
