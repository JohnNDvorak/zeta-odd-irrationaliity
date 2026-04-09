# Phase 2 symmetric-dual to baseline-dual annihilator transfer object spec

- Spec id: `bz_phase2_symmetric_dual_baseline_annihilator_transfer_object_spec`
- Prior packet-transfer hard wall: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_dual_baseline_transfer_decision_gate.md`
- Object label: `Symmetric-dual to baseline-dual local annihilator transfer object`
- Object kind: `paired_local_annihilator_profile_transfer_object`

## Source profile

- Object id: `bz_phase2_symmetric_dual_local_annihilator_profile`
- Family: `totally_symmetric_dual_f7_packet`
- Kind: `exact_local_annihilator_profile`
- Shared window: `n=1..77`
- Note: Local annihilator profile `(a_n, b_n, c_n)` induced by four consecutive symmetric dual packet vectors.

## Target profile

- Object id: `bz_phase2_baseline_dual_local_annihilator_profile`
- Family: `baseline_dual_f7_packet`
- Kind: `exact_local_annihilator_profile`
- Shared window: `n=1..77`
- Note: Local annihilator profile `(a_n, b_n, c_n)` induced by four consecutive baseline dual packet vectors.

## Transfer semantics

The active transfer object compares local annihilator profiles rather than packet coordinates. Each window encodes the exact recurrence geometry of four consecutive packet vectors, so the comparison is basis-free at the packet level and closer to recurrence structure.

## Rationale

Packet, pair, projective, and determinant-level transfer objects all exhausted their low-complexity ladders. The next natural object class is the local annihilator profile because it tests whether the obstruction survives after passing from packet coordinates to induced recurrence-level data.

## Source boundary

A transfer success would still be a bounded profile-level relation on `n=1..77`. It would not by itself prove family equivalence, a baseline recurrence, or a baseline remainder pipeline.

## Non-claims

- This spec does not claim the two local annihilator profiles are already equivalent.
- This spec does not prove a common minimal recurrence for the two packet families.
- This spec does not justify skipping the bounded transfer family ladder on the profile object.

## Recommended next step

Hash the paired local annihilator profiles first, then test one bounded low-complexity profile-map ladder.
