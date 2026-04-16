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
- raw/logs/bz_phase2_seven_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_affine_matrix_decision_gate.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_sym2_seven_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym2_eight_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_ladder_decision_gate.md
last_updated: '2026-04-15'
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
- Six-window normalized Plücker low-order global shared-scalar vector recurrences through order `10`.
- Six-window normalized Plücker low-order constant matrix recurrence through order `3`.
- Seven-window normalized Plücker low-order constant matrix recurrence through order `2`.
- Seven-window normalized Plücker low-order affine matrix recurrence through order `2`.
- Eight-window normalized Plücker order-`1` constant matrix recurrence.
- Sym2-lifted seven-window low-order constant matrix recurrence through order `10`.
- Sym2-lifted seven-window low-order affine matrix recurrence through order `10`.
- Sym2-lifted eight-window low-order constant matrix recurrence through order `2`.
- Sym2-lifted eight-window low-order affine matrix recurrence through order `2`.
- Sym3-lifted eleven-window low-order constant matrix recurrence through order `6`.
- Sym3-lifted eleven-window low-order affine matrix recurrence through order `6`.
- Sym4-lifted sixteen-window low-order constant matrix recurrence through order `4`.
- Sym4-lifted sixteen-window low-order affine matrix recurrence through order `3`.

## Rule

Do not retry any class above unless a new source-backed identity, symmetry, or recurrence-level reason changes the
object itself rather than merely enlarging the same fit family.
