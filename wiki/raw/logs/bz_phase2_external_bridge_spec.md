# Phase 2 external bridge spec

- Spec id: `bz_phase2_external_bridge_spec`
- Bridge id: `zudilin_2002_third_order_zeta5_bridge`
- Source: `Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)`
- Location: `Theorem 1, equations (1) and (2)`
- Literature verification report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_literature_verification_report.md`
- External calibration report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_calibration_check.md`
- Dual projection decision gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_decision_gate.md`

## Bridge object

- Published recurrence-based linear forms ℓ_n = q_n ζ(5) - p_n and ℓ̃_n = q_n ζ(3) - p̃_n

## Summary

Use the Zudilin 2002 third-order recurrence construction as the first implementation-calibration target. It is not the Brown-Zudilin baseline family, but it is explicit at the exact linear-form level and has the right two-channel shape for a controlled coefficient-side comparison.

## Why now

The dual projection decision gate chose the external bridge path because the baseline projection rule experiment remained bookkeeping-only. This bridge object is the strongest verified next target because it lets us compare an explicit published zeta(5)/zeta(3) linear-form structure against the repo's baseline dual-side conventions.

## Comparison fields

| field | target object | calibration anchor | comparison role |
| --- | --- | --- | --- |
| `leading_target_channel` | baseline dual F_7 retained `(constant, ζ(5))` pair | published `q_n ζ(5) - p_n` | Check whether the repo records the target odd-zeta channel with explicit coefficient bookkeeping instead of a scalar-only remainder. |
| `companion_channel` | baseline dual residual `ζ(3)` channel | published companion `q_n ζ(3) - p̃_n` | Check whether companion-channel handling is explicit and reproducible rather than hidden or discarded. |
| `sequence_level_object` | shared-window hashed packet / retained pair / residual channel | published recurrence-plus-initial-data sequence object | Record where the repo object is still weaker than the external bridge because it lacks a published recurrence and only has finite exact windows. |

## Implementation contract

- Do not try to rederive the full Zudilin 2002 construction immediately; first encode the bridge object as a comparison target with the three fields above.
- Keep the comparison one level above numerics: compare object shape, channel bookkeeping, and reproducibility assumptions before any performance-heavy extraction work.
- Treat a mismatch as useful information about the baseline dual conventions, not as a failure of the bridge path itself.

## Success condition

The next artifact names one explicit comparison target derived from Zudilin 2002 and states exactly how the baseline dual packet will be compared against it on the three bridge fields.
