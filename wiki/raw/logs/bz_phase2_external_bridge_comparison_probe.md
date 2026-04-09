# Phase 2 external bridge comparison probe

- Probe id: `bz_phase2_external_bridge_comparison_probe`
- Bridge target report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_comparison_target.md`
- Bridge spec report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_spec.md`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Partial fields: `leading_target_channel, companion_channel`
- Blocking fields: `sequence_level_object`

## Field verdicts

| field | baseline strength | bridge strength | verdict |
| --- | --- | --- | --- |
| `leading_target_channel` | explicit hashed coefficient-side object | published recurrence-backed linear-form channel | `structurally_partial` |
| `companion_channel` | explicit hashed coefficient-side object | published recurrence-backed linear-form channel | `structurally_partial` |
| `sequence_level_object` | finite exact windows only | recurrence plus initial data | `blocking_gap` |

## Explanations

- `leading_target_channel`: The baseline side is good enough to support channel-level comparison because the channel is explicit, hashed, and not hidden. It still falls short of the bridge object because it has not yet been promoted to a published-style recurrence-backed linear form.
- `companion_channel`: The baseline side is good enough to support channel-level comparison because the channel is explicit, hashed, and not hidden. It still falls short of the bridge object because it has not yet been promoted to a published-style recurrence-backed linear form.
- `sequence_level_object`: This remains the main blocker. The baseline side is reproducible only on shared finite windows, while the bridge object is sequence-explicit. Until that asymmetry is either reduced or deliberately accepted, the comparison cannot be stronger than structural.

## Overall verdict

The external bridge comparison is now concrete enough to be useful: two fields are structurally partial matches and one field is the clear blocker. That means the next productive artifact should not be another abstract spec. It should be a comparison note that explicitly accepts the finite-window asymmetry and then states one normalization-level comparison against Zudilin 2002.

## Next step

Write a normalization-level comparison note for the Zudilin 2002 bridge that explicitly compares the baseline retained `(constant, ζ(5))` pair and residual `ζ(3)` channel to the published bridge channels while accepting that the baseline side is finite-window rather than recurrence-explicit.
