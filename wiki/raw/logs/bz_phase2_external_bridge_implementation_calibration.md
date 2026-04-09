# Phase 2 external bridge implementation calibration

- Calibration id: `bz_phase2_external_bridge_implementation_calibration`
- Normalization note: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_normalization_note.md`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Retained pair hash: `c09c3939d1f2eda843de8f8a9191ab71ba9e14770a33cc0d9150b1b591e8cbc0`
- Residual channel hash: `a77ea420009d5ce76ed63e7c75bf1f63ad6832813958f196c8b8b81d870ea3c3`
- Readiness status: `ready_for_bridge_comparison_implementation`

## Accepted asymmetry

The baseline side is only finite-window exact on n=1..80, while the Zudilin 2002 bridge is recurrence-explicit. This note accepts that asymmetry and compares only normalization shape, channel bookkeeping, and reproducibility level.

## Calibration rules

### compare_channel_shape_only

- Allowed comparison: Compare the baseline retained `(constant, ζ(5))` pair to the published `q_n ζ(5) - p_n` bridge only at the level of channel shape, explicit coefficient bookkeeping, and reproducible indexing.
- Forbidden claim: Do not claim that the retained pair already equals a bridge-style recurrence-backed linear form.
- Required disclosure: State explicitly that the baseline side is finite-window exact while the bridge side is recurrence-explicit.

### compare_companion_channel_openly

- Allowed comparison: Compare the baseline residual `ζ(3)` channel to the published companion `q_n ζ(3) - p̃_n` bridge as an explicit companion-channel object.
- Forbidden claim: Do not treat the residual channel as eliminated, negligible, or already normalized away.
- Required disclosure: State that the baseline side carries the `ζ(3)` channel as residual data only, without a bridge-style recurrence.

### accept_sequence_strength_gap

- Allowed comparison: Use hashes and shared exact windows to compare reproducibility level and object shape.
- Forbidden claim: Do not present the baseline packet or retained pair as sequence-explicit in the same sense as the Zudilin 2002 bridge.
- Required disclosure: Name the finite-window versus recurrence-level asymmetry as the active blocker in every implementation-calibration artifact.

## Next artifact

Implement one bridge-comparison implementation note that applies these three rules directly to the baseline retained pair and residual `ζ(3)` channel against the Zudilin 2002 bridge channels.
