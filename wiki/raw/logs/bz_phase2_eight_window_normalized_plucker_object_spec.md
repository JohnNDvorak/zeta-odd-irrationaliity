# Phase 2 eight-window normalized Plucker object spec

- Spec id: `bz_phase2_eight_window_normalized_plucker_object_spec`
- Object label: `Symmetric-dual to baseline-dual eight-window normalized Plucker object`
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

For each eight-term packet window `(v_n, ..., v_{n+7})`, form the normalized `Gr(3,8)` Plucker coordinate vector by dividing all `3x3` minors by the pivot minor `(1,2,3)` and omitting the pivot coordinate.

## Rationale

The seven-window normalized Plucker object is now banked, and both the homogeneous and affine low-order constant-matrix ladders are exhausted there. The strongest remaining continuation is therefore a wider nonlinear invariant, with the first screen kept bounded to the last overdetermined matrix order.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared eight-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the eight-window source and target invariants are already equivalent.
- This object spec does not justify quotient or cross-ratio continuations, which were already weaker on smaller windows.
- This object spec does not claim higher matrix order is the right first screen once the order becomes underdetermined.

## Recommended next step

Hash the paired eight-window invariant first, then test only the overdetermined order-1 constant matrix recurrence on source and target separately.
