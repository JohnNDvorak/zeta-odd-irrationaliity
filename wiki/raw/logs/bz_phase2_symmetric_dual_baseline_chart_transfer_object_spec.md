# Phase 2 symmetric-dual to baseline-dual chart transfer object spec

- Spec id: `bz_phase2_symmetric_dual_baseline_chart_transfer_object_spec`
- Prior annihilator hard wall: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_dual_baseline_annihilator_transfer_decision_gate.md`
- Object label: `Symmetric-dual to baseline-dual chart-profile transfer object`
- Object kind: `paired_window_chart_profile_transfer_object`

## Source profile

- Object id: `bz_phase2_symmetric_dual_window_chart_profile`
- Family: `totally_symmetric_dual_f7_packet`
- Kind: `exact_window_chart_profile`
- Shared window: `n=1..76`
- Note: Five-term window chart profile that expresses columns 4 and 5 in the local chart determined by columns 1, 2, and 3 of each symmetric dual packet window.

## Target profile

- Object id: `bz_phase2_baseline_dual_window_chart_profile`
- Family: `baseline_dual_f7_packet`
- Kind: `exact_window_chart_profile`
- Shared window: `n=1..76`
- Note: Five-term window chart profile that expresses columns 4 and 5 in the local chart determined by columns 1, 2, and 3 of each baseline dual packet window.

## Transfer semantics

The active transfer object compares five-term window chart profiles. This is a richer subspace-level object than the 1D local annihilator profile: each window is represented by a 6-dimensional exact chart coordinate vector describing the induced 3-plane inside the five-column window.

## Rationale

Packet, projective, determinant, and local-annihilator transfer objects all exhausted their low-complexity ladders. The five-term chart profile is the next natural object class because it keeps exact windowed subspace geometry while remaining tractable enough for bounded exact family tests.

## Source boundary

A transfer success would still be a bounded chart-profile relation on `n=1..76`. It would not by itself prove packet equivalence, a common recurrence, or a baseline remainder pipeline.

## Non-claims

- This spec does not claim the two chart profiles are already equivalent.
- This spec does not prove a common recurrence for the symmetric and baseline dual packets.
- This spec does not justify importing symmetric identities into the baseline family.

## Recommended next step

Hash the paired chart profiles first, then test one bounded family ladder on the chart object.
