# Phase 2 Zudilin 2002 companion-channel-aware bridge ansatz

- Ansatz id: `bz_phase2_zudilin_2002_companion_channel_ansatz`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Shared exact window: `n=1..7`
- Comparison implementation note: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_bridge_comparison_implementation_note.md`
- Normalization decision gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_zudilin_2002_normalization_decision_gate.md`

- Ansatz label: Companion-channel-aware two-channel bridge ansatz

## Statement

Treat the baseline retained `ζ(5)` channel and the baseline residual `ζ(3)` channel as a coupled two-channel object, and compare that pair directly against the published Zudilin 2002 pair `(q_n ζ(5)-p_n, q_n ζ(3)-p̃_n)` instead of trying to normalize the `ζ(5)` channel alone by a low-degree scalar map.

## Why this follows

- The implementation note already requires the companion `ζ(3)` channel to remain explicit rather than hidden.
- The normalization decision gate closes the scalar/affine/quadratic one-channel rescaling line on the shared window.
- The external bridge object is itself naturally two-channel, so a coupled ansatz matches the published bridge shape better than another one-channel map.

## Coupled fields

| field | baseline object | bridge object | role |
| --- | --- | --- | --- |
| `target_channel` | baseline retained `ζ(5)` channel | published `q_n ζ(5) - p_n` channel | Primary odd-zeta target channel carried explicitly inside the coupled comparison. |
| `companion_channel` | baseline residual `ζ(3)` channel | published `q_n ζ(3) - p̃_n` channel | Companion channel that must remain visible and may participate in the transformation instead of being normalized away. |
| `coupled_object` | finite-window exact ordered pair `(ζ(5), ζ(3))` | published ordered bridge pair `(ℓ_n, ℓ̃_n)` | The real comparison object for the next phase: a two-channel ordered pair, not a single normalized scalar sequence. |

## Allowed outcome

A future probe may report that the baseline pair and bridge pair are compatible with some coupled finite-window transformation ansatz without claiming recurrence-level equivalence.

## Forbidden outcome

Do not claim that the baseline residual `ζ(3)` channel has been eliminated or that the baseline pair has already been converted into the published Zudilin recurrence object.

## Recommendation

The next concrete artifact should be a coupled two-channel comparison target or probe, built on the ordered pair `(baseline ζ(5), baseline ζ(3))` versus `(bridge ζ(5), bridge ζ(3))`, with the finite-window asymmetry kept explicit.
