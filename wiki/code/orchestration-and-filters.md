---
title: Orchestration and Structural Filters
category: code
phase: '1'
direction: '1'
sources:
- raw/code/orchestrator.py
- raw/code/gate0_parse.py
- raw/code/gate1_filter.py
last_updated: '2026-04-09'
---

Code page for the structural orchestration layer and the early filter gates that keep the search conservative.

These modules hold the non-notebook workflow together: parse input seeds, filter structural candidates, and route
them into exact or modular probe campaigns.
