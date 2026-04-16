---
title: Sym4 Sixteen-Window Affine Target Block Quotient Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_parity_support_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_block_quotient_screen.md
last_updated: '2026-04-16'
---

Audit record for quotienting the stable affine target `(order, degree) = (1, 2)` nullspace block.

## Scope

- Full affine target case: `960` equations, `723` unknowns
- Stable pre-quotient nullity: `150`
- Removed columns: `150`
- Removed pattern: degree-2 matrix coefficients `M[2,0,i,j]` for target index `i=0..14` and source index `j=5..14`
- Quotient unknowns: `573`
- Tested primes: `1451`, `1453`, `1471`, `1481`, `1483`, `1487`, `1489`, and `1493`

## Outcome

After removing exactly the stable free degree-2 matrix block, the quotient matrix is full column rank at every tested good prime:

- quotient rank `573`
- quotient nullity `0`

## Interpretation

The affine target `(order, degree) = (1, 2)` modular nullspace is accounted for by the visible parity-sparse degree-2 matrix block. This does not prove an exact rational theorem, but it removes the affine case as the best small recurrence-bearing lead.

## Next Action

Shift classification to the homogeneous target cases:

- homogeneous `(order, degree) = (1, 2)`, corrected nullity `150`
- homogeneous `(order, degree) = (1, 3)`, corrected nullity `360`
