# Phase 2 Sym^2-lifted eight-window object spec

- Spec id: `bz_phase2_sym2_eight_window_object_spec`
- Object label: `Sym^2-lifted eight-window normalized maximal-minor object`
- Object kind: `paired_schur_functor_window_invariant`

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

Lift each packet vector `(x,y,z)` to its `Sym^2` image `(x^2, xy, xz, y^2, yz, z^2)` in dimension `6`. For each eight-term lifted window, form the normalized maximal-minor coordinate vector in `Gr(6,8)` by dividing all `6x6` minors by the pivot minor of the first six columns and omitting that pivot coordinate.

## Rationale

The `Sym^2`-lifted seven-window object is now banked, and both its homogeneous and affine low-order matrix ladders are exhausted through order `10`. The strongest continuation inside the same lifted invariant family is therefore to widen the window once, because the resulting object still preserves an overdetermined matrix ladder through order `2` before interpolation takes over.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the lifted source and target invariants are already equivalent.
- This object spec does not claim widening the Sym^2 window is intrinsically stronger than changing the lifted representation.
- This object spec does not justify quotient or cheap order-escalation families on earlier normalized Plucker or Sym^2 seven-window objects.

## Recommended next step

Hash the paired Sym^2-lifted object first, then test the low-order homogeneous and affine constant-matrix recurrence ladders through the last overdetermined order.
