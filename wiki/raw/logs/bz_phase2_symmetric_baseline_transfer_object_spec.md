# Phase 2 symmetric-to-baseline transfer object spec

- Spec id: `bz_phase2_symmetric_baseline_transfer_object_spec`
- Prior baseline hard wall: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_full_packet_compression_decision_gate.md`
- Prior symmetric hard wall: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_source_packet_compression_decision_gate.md`
- Object label: `Symmetric-to-baseline packet transfer object`
- Object kind: `paired_source_target_exact_packet_transfer_object`

## Source packet

- Packet id: `bz_totally_symmetric_scaled_linear_forms_packet`
- Family: `totally_symmetric_linear_form_pipeline`
- Kind: `source_backed_scaled_exact_coefficient_packet`
- Shared window: `n=1..80`
- Note: Recurrence-explicit source-backed packet `(d_n^5 Q_n, d_n^5 P_n, d_n^2 d_{2n} P̂_n)`.

## Target packet

- Packet id: `bz_phase2_baseline_full_packet`
- Family: `baseline_dual_f7_packet`
- Kind: `baseline_side_exact_full_coefficient_packet`
- Shared window: `n=1..80`
- Note: Baseline dual full packet `(constant, zeta(3), zeta(5))` on the shared exact window.

## Transfer semantics

The active transfer object pairs a source-backed totally symmetric exact packet with the exact baseline dual full packet on the shared window `n=1..80`. It is a bounded transfer test bed, not a claim that the two families are already identified.

## Rationale

The baseline full packet and the symmetric source packet have each exhausted their own low-complexity internal pairwise compression ladders. The next honest move is to test whether a bounded exact packet-level transfer exists between the two families before enlarging either family internally.

## Source boundary

A transfer success would still be a packet-level relation on a finite exact window. It would not by itself prove baseline equivalence, baseline P_n extraction, or a baseline remainder pipeline.

## Non-claims

- This spec does not claim the symmetric family equals the baseline family.
- This spec does not claim the transfer object is motivic or canonical.
- This spec does not permit importing source-side recurrences as baseline-side recurrences without a proved transfer.

## Recommended next step

Hash the paired source/target packets first, then test one bounded low-complexity packet-map ladder.
