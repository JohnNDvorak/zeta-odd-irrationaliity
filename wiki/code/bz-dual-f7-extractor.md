---
title: bz_dual_f7.py Extractor and Kernel History
category: code
phase: '1'
direction: '6'
sources:
- raw/code/bz_dual_f7.py
- raw/logs/bz_phase2_dual_companion_checkpoint.md
last_updated: '2026-04-09'
---

Code page for the core exact dual F7 extractor and the six-round kernel-engineering history behind the frozen n=435 wall.

## Role

[`bz_dual_f7.py`] is the core exact extractor for dual `F_7` coefficient channels.

## History

The repo banked multiple kernel redesigns here: factorized rational paths, backend `mpq` fast paths, component
accumulators, reduced-fraction helpers, fused extraction logic, and hot-loop rewrites.

## Current status

The `n=435` wall is treated as architectural, not as a “one more micro-optimization” problem.
