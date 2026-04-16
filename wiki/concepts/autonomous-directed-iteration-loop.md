---
title: Autonomous Directed Iteration Loop
category: concept
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_autonomous_directed_iteration_loop.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md
last_updated: '2026-04-16'
---

Operational loop for continuing the repo-native research program without stopping after every recommendation.

## Cycle

1. Snapshot the current frontier, exhausted families, and git state.
2. Select one bounded candidate that is not a disguised retry of an exhausted family.
3. Run one bounded action: computation, decision gate, scoped helper, or synthesis repair.
4. Assess the outcome as `banked`, `hard_wall`, `promising_lead`, `engineering_wall`, `ill_posed`, or `do_not_retry`.
5. Recommend exactly one next action.
6. If the recommendation is auto-allowed, act on it immediately.
7. Bank, ingest, patch, rebuild index, lint, commit, and push before the next iteration.

## Auto-Allowed Actions

- Bank an already-produced result.
- Write or update a decision gate for a completed bounded screen.
- Implement a narrowly scoped helper for a selected bounded screen.
- Run an exact or modular obstruction screen on a banked/source-backed object when the tested range is strict overdetermined or has a stated structural reason.
- Patch stale wiki or handoff claims.
- Commit and push cleanly scoped artifacts.

## Stop Conditions

- The next candidate would invent non-symmetric baseline `P_n`.
- The next candidate reopens exact `n=435` without a new kernel architecture.
- The next candidate merely enlarges an exhausted bridge, packet, transfer, quotient, scalar, local, constant-matrix, or polynomial-matrix family.
- The next candidate is an interpolation search without a new structural reason.
- The next claim would confuse object-level success or obstruction evidence with recurrence-level proof.

## Current Use

The loop applies directly to the [[sym4-sixteen-window-object]] frontier. Its first post-loop autonomous iteration selected the generalized non-monic polynomial matrix family, ran the bounded screen, and found three target-side exact-follow-up cases. Its next iteration ran a bounded independent prime follow-up and found persistent modular nullity in all three cases.

The next loop action should extract/certify exact nullspace data for the smallest stable case, affine target-side `(order, degree) = (1, 2)`, before selecting another family.
