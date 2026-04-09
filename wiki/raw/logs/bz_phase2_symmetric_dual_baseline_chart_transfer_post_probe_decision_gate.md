# Phase 2 symmetric-dual to baseline-dual chart transfer post-probe decision gate

- Gate id: `bz_phase2_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_dual_baseline_chart_transfer_probe.md`
- Source probe id: `bz_phase2_symmetric_dual_baseline_chart_transfer_probe`
- Shared exact window: `n=1..76`
- Outcome: `continue_symmetric_dual_baseline_chart_transfer_family_probe`

| criterion | verdict | note |
| --- | --- | --- |
| `paired_exact_chart_profiles` | `satisfied` | Source and target are exact five-term chart profiles on the same shared window. |
| `reproducible_hashes` | `satisfied` | Source, target, and paired chart-transfer hashes are all reproducible. |
| `bounded_chart_family_choice` | `not_yet_satisfied` | No bounded chart-profile transfer family has been tested yet. |

## Rationale

The chart-profile object is strong enough to justify a bounded family ladder deeper than the previous low-complexity objects.

## Next step

Implement the bounded chart-family ladder with constant, difference, and support-1 through support-4 maps.

## Non-claims

- This does not claim the two chart profiles are equivalent.
- This does not prove a common recurrence for the symmetric and baseline dual packets.
- This does not justify importing symmetric identities into the baseline family.
