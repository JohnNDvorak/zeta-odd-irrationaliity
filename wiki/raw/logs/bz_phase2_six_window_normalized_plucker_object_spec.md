# Phase 2 six-window normalized Plucker object spec

- Spec id: `bz_phase2_six_window_normalized_plucker_object_spec`
- Object label: `Symmetric-dual to baseline-dual six-window normalized Plucker object`
- Object kind: `paired_nonlinear_grassmannian_window_invariant`

## Source packet

- Packet id: `bz_phase2_symmetric_dual_full_packet`
- Family: `totally_symmetric_dual_f7_packet`
- Kind: `exact_full_coefficient_packet`
- Shared window: `n=1..80`
- Note: Exact symmetric dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.

## Target packet

- Packet id: `bz_phase2_baseline_full_packet`
- Family: `baseline_dual_f7_packet`
- Kind: `exact_full_coefficient_packet`
- Shared window: `n=1..80`
- Note: Exact baseline dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.

## Invariant definition

For each six-term packet window `(v_n, ..., v_{n+5})`, form the normalized `Gr(3,6)` Plucker coordinate vector by dividing all `3x3` minors by the pivot minor `(1,2,3)` and omitting the pivot coordinate.

## Rationale

The five-term normalized Plucker object improved the transfer frontier, and the six-term follow-up screen improved it again at the cheap end. The next bounded direction is therefore a recurrence-level family on the full six-window nonlinear invariant rather than another quotient family.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared six-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the six-window source and target invariants are already equivalent.
- This object spec does not justify projective or cross-ratio quotient continuations, which are already weaker.
- This object spec does not claim support-depth escalation is the right next move on its own.

## Recommended next step

Hash the paired six-window invariant first, then test cheap constant/difference families and one different support-1 family with canonical free-zero resolution.
