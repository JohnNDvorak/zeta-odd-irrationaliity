# Phase 2 Sym^2-lifted seven-window object spec

- Spec id: `bz_phase2_sym2_seven_window_object_spec`
- Object label: `Sym^2-lifted seven-window normalized maximal-minor object`
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

Lift each packet vector `(x,y,z)` to its `Sym^2` image `(x^2, xy, xz, y^2, yz, z^2)` in dimension `6`. For each seven-term lifted window, form the normalized maximal-minor coordinate vector in `Gr(6,7)` by dividing all `6x6` minors by the pivot minor of the first six columns and omitting that pivot coordinate.

## Rationale

Width-only normalized Plucker objects are now exhausted through the eight-window frontier at their cheap constant-matrix screens. The strongest beyond-Plucker continuation is therefore a Schur-functor lift that changes the invariant family itself while preserving exact arithmetic.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Non-claims

- This object spec does not claim the lifted source and target invariants are already equivalent.
- This object spec does not claim the Sym^2 lift is the unique or final Schur-functor continuation.
- This object spec does not justify retrying quotient or cheap order-escalation families on the earlier normalized Plucker objects.

## Recommended next step

Hash the paired Sym^2-lifted object first, then test the low-order constant matrix recurrence ladder through the last overdetermined order.
