# Phase 2 seven-window normalized Plucker object spec

- Spec id: `bz_phase2_seven_window_normalized_plucker_object_spec`
- Object label: `Symmetric-dual to baseline-dual seven-window normalized Plucker object`
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

For each seven-term packet window `(v_n, ..., v_{n+6})`, form the normalized `Gr(3,7)` Plucker coordinate vector by dividing all `3x3` minors by the pivot minor `(1,2,3)` and omitting the pivot coordinate.

## Rationale

The six-window normalized Plucker object survived four different recurrence-level screens, but each cheap family is now exhausted there. The next defensible object-class pivot is therefore the wider seven-window normalized invariant, not another quotient or cheap family on the six-window object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared seven-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the seven-window source and target invariants are already equivalent.
- This object spec does not justify quotient or cross-ratio continuations, which were already weaker on smaller windows.
- This object spec does not claim support-depth escalation is the right first family at this larger coordinate count.

## Recommended next step

Hash the paired seven-window invariant first, then test the low-order constant matrix recurrence ladder only through the last overdetermined order.
