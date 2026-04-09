# Phase 2 external bridge normalization note

- Note id: `bz_phase2_external_bridge_normalization_note`
- Bridge spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_spec.md`
- Comparison probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_comparison_probe.md`
- Baseline rule experiment: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_rule_experiment.md`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Baseline source hash: `8dde8e0e3dca2ced6b0b96eea05422f5afdf497e54e0a812c8b977a7ba9cca6a`
- Retained pair hash: `c09c3939d1f2eda843de8f8a9191ab71ba9e14770a33cc0d9150b1b591e8cbc0`
- Residual channel hash: `a77ea420009d5ce76ed63e7c75bf1f63ad6832813958f196c8b8b81d870ea3c3`

## Accepted sequence asymmetry

The baseline side is only finite-window exact on n=1..80, while the Zudilin 2002 bridge is recurrence-explicit. This note accepts that asymmetry and compares only normalization shape, channel bookkeeping, and reproducibility level.

## Channel comparisons

### leading_target_channel

- Baseline normalization: retained `(constant, ζ(5))` coefficient-side pair on the shared exact window
- Bridge normalization: published linear form `q_n ζ(5) - p_n`
- Accepted asymmetry: The baseline object is a hashed retained pair, not yet a recurrence-backed linear form.
- Comparison statement: These are comparable at the normalization level because both keep the target odd-zeta channel explicit rather than collapsing it into a single opaque remainder.

### companion_channel

- Baseline normalization: explicit residual `ζ(3)` channel carried alongside the retained pair
- Bridge normalization: published companion linear form `q_n ζ(3) - p̃_n`
- Accepted asymmetry: The baseline side records the companion channel as residual data only; it does not yet derive a bridge-style companion recurrence.
- Comparison statement: These are comparable at the normalization level because the companion channel is explicit and reproducible on both sides instead of being hidden or silently discarded.

### sequence_level_object

- Baseline normalization: finite-window packet / retained-pair / residual-channel hashes
- Bridge normalization: published recurrence plus initial data
- Accepted asymmetry: This is the active blocker: the baseline side is sequence-addressable only by finite windows, while the bridge side is globally sequence-explicit.
- Comparison statement: These are not yet comparable as equal-strength sequence objects. The correct normalization-level statement is simply that the baseline side has reached reproducible finite-window exactness, not recurrence-level explicitness.

## Overall note

The normalization-level comparison is now explicit enough to support a stronger implementation-calibration step. The baseline side already matches the Zudilin 2002 bridge in the way it exposes the target and companion channels, but not in sequence-level strength.

## Next step

Use this note to drive one implementation-calibration artifact that compares the baseline retained pair and residual channel to the Zudilin 2002 bridge channels without claiming recurrence-level equivalence.
