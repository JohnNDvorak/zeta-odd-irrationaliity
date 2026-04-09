---
title: Bounded Refinement Ladder
category: concept
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_baseline_residual_refinement_decision_gate.md
- raw/logs/bz_phase2_baseline_odd_residual_refinement_decision_gate.md
- raw/logs/bz_phase2_baseline_full_packet_compression_decision_gate.md
last_updated: '2026-04-09'
---

The recurring same-index -> difference -> lagged-support pattern that marks a structural wall across packet and transfer directions.

## Pattern

Across packet compression, transfer, and refinement directions, the same bounded ladder recurs:

1. same-index support-0 family
2. consecutive-difference family
3. lagged support family

The direction either:

- fails right after its fit block, or
- becomes ill-posed at the first richer support level.

## Interpretation

When a new direction hits this pattern, the safe default is to classify it as the same structural obstruction rather
than escalating degree/support mechanically.

## Related pages

- [[exhausted-ansatz-classes]]
- [[six-window-normalized-plucker-object]]
