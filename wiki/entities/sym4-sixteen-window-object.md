---
title: Sym4 Sixteen-Window Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_object_spec.md
- raw/logs/bz_phase2_sym4_sixteen_window_probe.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_203158.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_ladder_decision_gate.md
- raw/logs/bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md
last_updated: '2026-04-16'
---

Current strongest higher-Schur frontier object, built by lifting each packet vector through `Sym^4` and then taking a sixteen-window normalized maximal-minor invariant in dimension `15`.

## Status

This is now a banked repo-native exact paired object, superseding the [[sym3-eleven-window-object]] as the strongest established higher-Schur invariant.

- It changes the invariant family from the cubic `Sym^3` lift to a quartic `Sym^4` lift.
- It is established exactly as a paired lifted invariant on `n=1..65`.
- It has coordinate count `15`.
- Its source invariant hash is `fc9ceb94cfd7c56b98d3f69c2a3efb4e7e47020e3fd1a8be628bf173d9dd476e`.
- Its target invariant hash is `216eede544444133c25cd8b82e1b83b991f54d3183c347f2351aed29dbedfc09`.
- Its paired object hash is `dfe18fe136e64e09be99280cd26919bb5e28219f81847e73d7dbfca7ee85b606`.
- Its homogeneous constant-matrix recurrence ladder is closed through order `4` on both sides.
- Its affine matrix recurrence ladder is closed through order `3` on both sides.
- Its strict overdetermined low-degree polynomial matrix extension is closed on both sides.
- Its non-monic polynomial matrix extension has three target-side exact-nullspace follow-up cases after a bounded prime sweep.

## Boundaries

- No recurrence-level transfer family has yet been certified on this object.
- The constant and polynomial matrix screens are hard walls, not recurrence successes.
- No implication for baseline `P_n` extraction follows directly from this object alone.
- No claim is made that the quartic Schur lift dominates every other higher nonlinear invariant family.

## Reading

This object matters because the former target-side quartic compute wall has been crossed by a persisted exact cache and final sequence-cache materialization. The constant-coefficient and monic low-degree polynomial matrix follow-ups are hard walls, while the non-monic polynomial screen now supplies a precise target-side exact-nullspace lead.

See [[sym4-sixteen-window-frontier]], [[sym4-sixteen-window-matrix-recurrence-screen]], [[sym4-sixteen-window-affine-matrix-screen]], [[sym4-sixteen-window-polynomial-matrix-screen]], [[sym4-sixteen-window-generalized-polynomial-matrix-screen]], [[sym4-sixteen-window-generalized-polynomial-matrix-followup]], [[sym4-generalized-polynomial-matrix-lead]], [[sym4-matrix-ladders-exhausted]], [[sym4-sixteen-window-target-partial-cache-progress]], [[sym4-sixteen-window-compute-wall]], and [[sym3-eleven-window-object]].
