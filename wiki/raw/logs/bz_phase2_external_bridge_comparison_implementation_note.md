# Phase 2 external bridge comparison implementation note

- Note id: `bz_phase2_external_bridge_comparison_implementation_note`
- Implementation calibration: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_implementation_calibration.md`
- Normalization note: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_normalization_note.md`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Retained pair hash: `c09c3939d1f2eda843de8f8a9191ab71ba9e14770a33cc0d9150b1b591e8cbc0`
- Residual channel hash: `a77ea420009d5ce76ed63e7c75bf1f63ad6832813958f196c8b8b81d870ea3c3`

## Accepted asymmetry

The baseline side is only finite-window exact on n=1..80, while the Zudilin 2002 bridge is recurrence-explicit. This note accepts that asymmetry and compares only normalization shape, channel bookkeeping, and reproducibility level.

## Implementation items

### leading_target_channel

- Baseline object: baseline retained `(constant, ζ(5))` pair
- Bridge object: published `q_n ζ(5) - p_n` bridge channel
- Allowed statement: The baseline side and the bridge side are comparable as explicit target-channel objects with named odd-zeta structure and reproducible indexing.
- Forbidden statement: Do not state or imply that the baseline retained pair is already the same kind of recurrence-backed linear form as `q_n ζ(5) - p_n`.

### companion_channel

- Baseline object: baseline residual `ζ(3)` channel
- Bridge object: published companion `q_n ζ(3) - p̃_n` bridge channel
- Allowed statement: The baseline side and the bridge side are comparable as explicit companion-channel objects that remain visible rather than being silently discarded.
- Forbidden statement: Do not claim that the baseline residual `ζ(3)` channel has been analytically eliminated or normalized into the target channel.

### sequence_level_object

- Baseline object: finite-window hashed packet / retained-pair / residual-channel objects
- Bridge object: published recurrence plus initial data
- Allowed statement: The baseline side can only be compared to the bridge side as a finite-window exact object with weaker sequence-level strength.
- Forbidden statement: Do not present the baseline side as sequence-explicit in the same sense as the Zudilin 2002 bridge.

## Implementation verdict

The bridge comparison is now implementable in a disciplined way: compare explicit target and companion channels directly, but carry the finite-window versus recurrence asymmetry as a permanent disclaimer rather than trying to hide it.

## Next step

Use this note as the stable rulebook for any later bridge-comparison code or report. The next genuinely new mathematical move would be either to shrink the sequence-strength gap or to find a stronger bridge object, not to restate the same comparison again.
