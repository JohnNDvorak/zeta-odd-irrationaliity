---
title: Sym4 Sixteen-Window Affine Target Nullspace Fingerprint
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup__20260416_123223.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_parity_support_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_block_quotient_screen.md
last_updated: '2026-04-16'
---

Audit record for the modular nullspace fingerprint of the smallest corrected target-side generalized polynomial matrix case.

## Scope

- Object: [[sym4-sixteen-window-object]]
- Case: affine target-side `(order, degree) = (1, 2)`
- Equations / unknowns: `960 / 723`
- Tested primes: `1451`, `1453`, `1471`, `1481`, `1483`, `1487`, `1489`, and `1493`

## Outcome

All tested good primes have the same corrected rank and nullity:

- rank `573`
- nullity `150`
- pivot count `573`
- verified nullspace row rank `150`

The free-column profile is stable across all tested primes. It consists of the degree-2 matrix coefficients
`M[2,0,i,j]` for target index `i=0..14` and source index `j=5..14`, i.e. `150` free columns.

## Correction Note

This supersedes the earlier ten-dimensional affine target nullity impression. The earlier follow-up used the direct `DomainMatrix(rows, shape, GF(p))` constructor, which gave inconsistent finite-field rank/RREF behavior on these matrices. The corrected code uses `DomainMatrix.from_list(rows, GF(p))` and verifies nullspace rows directly against the modular matrix.

## Interpretation

The affine target case is no longer a small exact-nullspace extraction target. Its stable `150`-dimensional modular nullspace looks structured, and the free columns all live in one visible degree-2 matrix block.

This still does not prove an exact rational recurrence. The next bounded action is to decide whether this large nullspace is mostly a gauge/coordinate freedom of the generalized affine family or whether a smaller canonical exact subspace survives after quotienting that freedom.

## Parity Support

The target sequence has a simple support pattern:

- coordinate `0` is nonzero for every `n=1..65`
- coordinates `1..14` are nonzero exactly on odd `n`
- coordinates `1..14` vanish on every even `n`

For order-1 target-side rows, that means the history vector at `n-1` has coordinates `1..14` active only when the target index `n` is even. The stable free columns are therefore not globally unused columns; they sit in a parity-sparse degree-2 matrix block.

## Block Quotient

Removing exactly the `150` stable free columns leaves a quotient system with `573` unknowns. That quotient has full column rank `573` at every tested good prime.

This means the affine target nullspace is accounted for by the visible parity-sparse degree-2 matrix block; it is no longer the best candidate for exact recurrence extraction.
