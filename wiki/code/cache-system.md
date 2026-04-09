---
title: Cache System
category: code
phase: '1'
direction: '4'
sources:
- raw/code/dual_f7_exact_coefficient_cache.py
- raw/logs/bz_dual_f7_exact_probe_report.md
last_updated: '2026-04-09'
---

Code page for exact cache management of the dual coefficient channels and companion objects.

The cache system stores exact channel data and derived probe outputs so exact windows can be reused without recomputing
the whole extraction stack.
