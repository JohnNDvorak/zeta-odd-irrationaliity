# Phase 2 Sym^4-lifted sixteen-window object spec

- Spec id: `bz_phase2_sym4_sixteen_window_object_spec`
- Object label: `Sym^4-lifted sixteen-window normalized maximal-minor object`
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

Lift each packet vector `(x,y,z)` to its `Sym^4` image in dimension `15`, using the quartic monomial basis `(x^4, x^3y, x^3z, x^2y^2, x^2yz, x^2z^2, xy^3, xy^2z, xyz^2, xz^3, y^4, y^3z, y^2z^2, yz^3, z^4)`. For each sixteen-term lifted window, form the normalized maximal-minor coordinate vector in `Gr(15,16)` by dividing all `15x15` minors by the pivot minor of the first fifteen columns and omitting that pivot coordinate.

## Rationale

The `Sym^3`-lifted eleven-window object is now banked. The strongest continuation inside the higher-Schur line is a quartic lift that still leaves a genuinely overdetermined homogeneous ladder through order `4` and an affine ladder through order `3`.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the lifted source and target invariants are already equivalent.
- This object spec does not claim the quartic Schur lift is final or optimal among higher nonlinear invariants.
- This object spec does not justify retrying exhausted low-order families on the earlier Sym^2 or Sym^3 objects.

## Recommended next step

Hash the paired Sym^4-lifted object first, then test the low-order homogeneous matrix ladder through order `4` and the affine ladder through order `3`.
