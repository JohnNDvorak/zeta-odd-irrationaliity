---
title: Sym4 Sixteen-Window Compute Wall
category: audit
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_compute_wall_note.md
last_updated: '2026-04-09'
---

Audit record for the attempted quartic higher-Schur continuation beyond the banked [[sym3-eleven-window-object]].

## Object and status

- Draft object: `Sym^4`-lifted sixteen-window normalized maximal-minor object
- Intended coordinate count: `15`
- Intended shared exact window: `n=1..65`
- Status: `compute wall`, not banked

## What was established

- The quartic lift support was added to the higher-Schur helper layer.
- The codimension-one normalized maximal-minor solver was improved from direct `Fraction` elimination to row-scaled integer elimination with rational back-substitution.
- Low-level exact arithmetic checks stayed green after that solver change.

## Failure mode

The first full quartic tranche did not produce a banked object within practical turn-time:

- before the solver rewrite, the quartic pytest tranche ran at saturated CPU for more than `9` minutes without completing
- after the solver rewrite, the quartic pytest tranche again ran at saturated CPU for more than `9` minutes without completing

Live process sampling showed the remaining hotspot inside exact integer floor-division work during fraction-free elimination in the codimension-one solver.

## Interpretation

This is an engineering blocker, not a mathematical obstruction result:

- `Sym^4` sixteen-window has **not** been certified as a new frontier object
- the stable banked higher-Schur frontier remains [[sym3-eleven-window-object]]
- resuming the quartic line would require stronger determinant or minor reuse, cached elimination structure across adjacent windows, or a cheaper nonlinear invariant family
