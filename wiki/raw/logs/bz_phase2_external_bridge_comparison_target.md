# Phase 2 external bridge comparison target

- Target id: `bz_phase2_external_bridge_comparison_target`
- Bridge spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_spec.md`
- Baseline projection probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_probe.md`
- Baseline projection rule experiment: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_rule_experiment.md`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Comparison mode: `shape_and_reproducibility_before_recurrence`
- Overall status: `ready_for_comparison_probe`

## Comparison fields

### leading_target_channel

- Baseline object: retained `(constant, ζ(5))` pair from the baseline dual projection rule experiment
- Bridge object: published `q_n ζ(5) - p_n` linear form
- Current status: `partially_aligned`
- Current evidence: The baseline side now has a retained-pair hash `c09c3939d1f2eda843de8f8a9191ab71ba9e14770a33cc0d9150b1b591e8cbc0` on the shared exact window n=1..80, so the target odd-zeta channel is explicit at the coefficient level. It is still weaker than the bridge object because it is not yet a published or derived recurrence-based linear form.
- Next required artifact: A comparison probe that states one explicit normalization map from the retained pair to the published `q_n ζ(5) - p_n` shape.

### companion_channel

- Baseline object: explicit residual `ζ(3)` channel from the baseline dual projection rule experiment
- Bridge object: published companion `q_n ζ(3) - p̃_n` linear form
- Current status: `partially_aligned`
- Current evidence: The baseline side carries a residual-channel hash `a77ea420009d5ce76ed63e7c75bf1f63ad6832813958f196c8b8b81d870ea3c3` instead of hiding the companion channel. That matches the bridge path at the bookkeeping level, but not yet at the level of a recurrence-backed companion linear form.
- Next required artifact: A comparison probe that states how the residual `ζ(3)` channel is to be compared to the published companion bridge object without pretending they are already the same kind of sequence.

### sequence_level_object

- Baseline object: shared-window hashed packet / retained pair / residual channel
- Bridge object: published recurrence-plus-initial-data sequence object
- Current status: `not_yet_aligned`
- Current evidence: The baseline side is reproducible only as finite exact windows, with source packet hash `8dde8e0e3dca2ced6b0b96eea05422f5afdf497e54e0a812c8b977a7ba9cca6a` on n=1..80. The bridge object is stronger because it comes with an explicit recurrence and initial data.
- Next required artifact: A comparison note that records this asymmetry explicitly and refuses to overstate the baseline object as sequence-explicit.

## Next step

Write one comparison probe that takes these three fields and produces a single report saying where the baseline dual packet already matches the Zudilin 2002 bridge structurally and where it still falls short.
