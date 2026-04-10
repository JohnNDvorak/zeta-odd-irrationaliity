# Phase 2 Sym^3-lifted eleven-window object spec

- Spec id: `bz_phase2_sym3_eleven_window_object_spec`
- Object label: `Sym^3-lifted eleven-window normalized maximal-minor object`
- Object kind: `paired_higher_schur_window_invariant`

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

Lift each packet vector `(x,y,z)` to its `Sym^3` image in dimension `10`, using the cubic monomial basis `(x^3, x^2 y, x^2 z, x y^2, x y z, x z^2, y^3, y^2 z, y z^2, z^3)`. For each eleven-term lifted window, form the normalized maximal-minor coordinate vector in `Gr(10,11)` by dividing all `10x10` minors by the pivot minor of the first ten columns and omitting that pivot coordinate.

## Rationale

The `Sym^2`-lifted seven-window and eight-window objects are now banked. The strongest structurally different continuation is therefore a higher Schur lift that still leaves a genuine overdetermined matrix ladder through order `6`.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^3-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the lifted source and target invariants are already equivalent.
- This object spec does not claim the cubic Schur lift is uniquely preferred over every other nonlinear invariant family.
- This object spec does not justify retrying richer families on the already exhausted Sym^2 or normalized Plucker objects.

## Recommended next step

Hash the paired Sym^3-lifted object first, then test the low-order homogeneous and affine matrix recurrence ladders through the last overdetermined order.
