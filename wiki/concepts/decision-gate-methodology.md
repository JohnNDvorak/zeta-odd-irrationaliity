---
title: Decision-Gate Methodology
category: concept
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_pivot_report.md
- raw/code/baseline_residual_refinement_decision_gate.py
- raw/code/symmetric_dual_baseline_chart_transfer_decision_gate.py
last_updated: '2026-04-09'
---

Program rule that every bounded lane must end in an explicit banked outcome, hard wall, or frontier recommendation.

Decision gates record:

- object tested
- parameter range
- family class
- exact window size
- failure mode or certified outcome

This prevents the repo from re-deriving the same dead ends and is one of the main positive outputs of the program.
