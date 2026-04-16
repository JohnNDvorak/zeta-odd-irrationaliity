---
title: Sym4 Sixteen-Window Polynomial Matrix Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen.md
last_updated: '2026-04-15'
---

Audit record for the low-degree polynomial-coefficient matrix family on the [[sym4-sixteen-window-object]].

## Object and family

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor sequence
- Family: matrix-valued recurrences with low-degree polynomial coefficients in the target index `n`
- Sides tested independently: source and target
- Shared exact object window: `n=1..65`

## Certified failure mode

This screen is certified by finite-field obstruction across every strict overdetermined low-degree polynomial matrix case that remains after the constant-coefficient ladders close:

- homogeneous `(order, degree) = (1, 1)`, `(1, 2)`, `(1, 3)`, and `(2, 1)`
- affine `(order, degree) = (1, 1)`, `(1, 2)`, and `(2, 1)`
- source-side witness prime `1009`
- target-side witness prime `1451`

Since inconsistency mod `p` implies inconsistency over `Q`, this closes the bounded polynomial-coefficient extension of the Sym4 matrix screen over its strict overdetermined range.

## Boundary

- Homogeneous `(order, degree) = (1, 4)` has `1125` unknowns against `960` equations.
- Homogeneous `(order, degree) = (2, 2)` has `1350` unknowns against `945` equations.
- Affine `(order, degree) = (1, 3)` has `960` unknowns against `960` equations.
- Affine `(order, degree) = (2, 2)` has `1395` unknowns against `945` equations.

So further escalation would stop being a strict overdetermined obstruction screen and would need a separate structural reason.

## Implementation Note

The screen uses direct modular row construction and prioritizes the known source/target witness primes. This avoids the expensive Fraction-to-mod sweep that made the first prototype unsuitable for the target side.
