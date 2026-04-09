---
title: Exhausted Ansatz Classes
category: conclusion
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_literature_verification_report.md
- raw/logs/bz_phase2_plucker_quotient_family_screen.md
- raw/logs/bz_phase2_six_window_plucker_followup_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Tracked ledger of ansatz classes that should not be retried without a new structural reason.

## Exhausted classes

- Low-order / low-degree recurrence families on baseline `Q_n`.
- Dual companion `(1,0,-1,-2)` polynomial recurrence family through degree `106`.
- Zudilin-bridge scalar normalization maps.
- Zudilin-bridge affine normalization maps.
- Zudilin-bridge quadratic normalization maps.
- Zudilin-bridge constant coupled `2x2` map.
- Baseline packet compression on `(constant, ζ(5))`, `(ζ(5), ζ(3))`, and full packet.
- Symmetric source packet compression.
- Symmetric-to-baseline and symmetric-dual-to-baseline-dual low-complexity transfer maps.
- Local annihilator transfer maps in the same bounded family.
- Plücker quotient and cross-ratio quotient families.
- Six-window normalized Plücker constant and difference transfer families.
- Six-window normalized Plücker canonical free-zero support-1 family.
- Six-window normalized Plücker short local-annihilator families of relation length `4`, `5`, and `6`.

## Rule

Do not retry any class above unless a new source-backed identity, symmetry, or recurrence-level reason changes the
object itself rather than merely enlarging the same fit family.
