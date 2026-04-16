---
title: Sym4 Sixteen-Window Generalized Polynomial Matrix Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
last_updated: '2026-04-16'
---

Audit record for the non-monic polynomial-coefficient matrix family on the [[sym4-sixteen-window-object]].

## Object and family

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor sequence
- Family: matrix-valued recurrences with low-degree polynomial coefficients in the target index `n`
- Extra freedom beyond [[sym4-sixteen-window-polynomial-matrix-screen]]: a scalar polynomial coefficient is allowed on the target vector
- Sides tested independently: source and target
- Shared exact object window: `n=1..65`

## Outcome

This is a live follow-up lead, not a hard wall.

The screen found full-column-rank modular obstructions for most strict overdetermined cases:

- all source-side cases tested are full column rank mod prime `1009`
- most target-side cases tested are full column rank mod prime `1451`

But no full-rank modular obstruction was found at the known witness primes for three target-side cases:

- homogeneous `(order, degree) = (1, 2)` with `960` equations and `678` unknowns
- homogeneous `(order, degree) = (1, 3)` with `960` equations and `904` unknowns
- affine `(order, degree) = (1, 2)` with `960` equations and `723` unknowns

## Boundary

The result does not prove that any target-side recurrence exists. It says the modular full-rank obstruction used by the bounded screen did not close those three cases at the known witness primes, so exact follow-up is required before either banking a recurrence lead or declaring the generalized family exhausted.

## Implementation Note

The screen uses direct modular vector conversion, SymPy finite-field `DomainMatrix.rank()` when available, and the known source/target witness-prime pair. It deliberately does not sweep a large prime list, because the loop treats missing full-rank obstruction at the known witnesses as an exact-follow-up lead rather than an invitation to unbounded prime search.
