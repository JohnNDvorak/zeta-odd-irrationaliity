# Phase 2 symmetric-dual to baseline-dual transfer object spec

- Spec id: `bz_phase2_symmetric_dual_baseline_transfer_object_spec`
- Prior baseline packet hard wall: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_full_packet_compression_decision_gate.md`
- Prior mixed-family transfer hard wall: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_baseline_transfer_decision_gate.md`
- Object label: `Symmetric-dual to baseline-dual transfer object`
- Object kind: `paired_exact_dual_packet_transfer_object`

## Source packet

- Packet id: `bz_phase2_symmetric_dual_full_packet`
- Family: `totally_symmetric_dual_f7_packet`
- Kind: `exact_full_coefficient_packet`
- Shared window: `n=1..80`
- Note: Symmetric dual full packet `(constant, zeta(3), zeta(5))` from the same exact F_7 extraction family.

## Target packet

- Packet id: `bz_phase2_baseline_full_packet`
- Family: `baseline_dual_f7_packet`
- Kind: `exact_full_coefficient_packet`
- Shared window: `n=1..80`
- Note: Baseline dual full packet `(constant, zeta(3), zeta(5))` on the same shared exact window.

## Transfer semantics

The active transfer object pairs the symmetric dual F_7 full packet with the baseline dual F_7 full packet. This is the most structurally aligned packet-transfer object currently available: same extraction family, same coefficient basis, same exact window.

## Rationale

The mixed symmetric-source to baseline transfer object exhausted its low-complexity ladder. The strongest remaining different transfer object is the direct dual-to-dual packet pairing, because it removes the family-type mismatch and tests whether the obstruction survives inside a single exact extraction framework.

## Source boundary

A transfer success would still be a bounded packet-level relation on `n=1..80`. It would not by itself prove baseline equivalence, a baseline recurrence, or a baseline remainder pipeline.

## Non-claims

- This spec does not claim the symmetric dual packet and the baseline dual packet are already equivalent.
- This spec does not import symmetric identities into the baseline packet without a proved transfer.
- This spec does not justify skipping the bounded transfer family ladder.

## Recommended next step

Hash the paired dual packets first, then test one bounded low-complexity packet-map ladder.
