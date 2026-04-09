---
title: Decision-Gate Artifact Writers
category: code
phase: '2'
direction: frontier
sources:
- raw/code/campaign_report.py
- raw/code/baseline_residual_refinement_decision_gate.py
- raw/code/symmetric_dual_baseline_chart_transfer_decision_gate.py
last_updated: '2026-04-09'
---

Code page for the report-writing pattern that turns every probe family into a traceable gate or checkpoint artifact.

These modules exemplify the repo-native pattern: generate exact outputs, write markdown and JSON artifacts, and bank
hard walls in a way that the wiki can ingest cleanly.
