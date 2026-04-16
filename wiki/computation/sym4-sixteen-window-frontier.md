---
title: Sym4 Sixteen-Window Frontier
category: computation
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
last_updated: '2026-04-15'
---

Current higher-Schur frontier: the `Sym^4`-lifted sixteen-window object is now the strongest **banked** exact paired invariant. Its constant-coefficient matrix ladders and strict overdetermined low-degree polynomial matrix extension are closed as hard walls.

## Object summary

- The `Sym^4`-lifted sixteen-window object is established exactly on `n=1..65`.
- It has coordinate count `15`.
- The paired object hash is `dfe18fe136e64e09be99280cd26919bb5e28219f81847e73d7dbfca7ee85b606`.
- The target-side cache reached `65 / 65` exact windows and materialized `data/cache/bz_phase2_sym4_sixteen_window_target_sequence_cache.json`.
- The final target sequence cache is `131681112` bytes.

## What Changed

The previous state was an engineering-only quartic continuation: the source side was tractable, but the target side had to be advanced by a persisted cache through alternating ordinary and rebase steps. That cache is now complete, and the default loader has been patched to parse the large cached fractions without requiring an external Python digit-limit override.

## Homogeneous Screen

- Source-side homogeneous orders `1..4` are inconsistent mod prime `1009`.
- Target-side homogeneous orders `1..4` are inconsistent mod prime `1451`.
- Order `4` is the last overdetermined homogeneous case, with `900` unknowns against `915` equations.
- Order `5` is underdetermined, with `1125` unknowns against `900` equations.

## Affine Screen

- Source-side affine orders `1..3` are inconsistent mod prime `1009`.
- Target-side affine orders `1..3` are inconsistent mod prime `1451`.
- Affine order `3` has `690` unknowns against `930` equations.
- Affine order `4` is no longer overdetermined, with `915` unknowns against `915` equations.

## Polynomial Matrix Screen

- Homogeneous polynomial-coefficient cases `(order, degree) = (1, 1)`, `(1, 2)`, `(1, 3)`, and `(2, 1)` are inconsistent on source and target.
- Affine polynomial-coefficient cases `(order, degree) = (1, 1)`, `(1, 2)`, and `(2, 1)` are inconsistent on source and target.
- The source witness prime is `1009`.
- The target witness prime is `1451`.

## Reading

This is a genuine mathematical frontier advance at the object level, with the natural matrix hard walls now banked on the quartic object. It is still not a proof-side recurrence success: no baseline extraction or common transfer recurrence follows from these obstructions, and [[sym4-matrix-ladders-exhausted]] records the decision not to continue by mechanical matrix-order or polynomial-degree escalation.
