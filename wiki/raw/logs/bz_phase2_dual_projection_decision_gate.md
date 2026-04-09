# Phase 2 dual projection decision gate

- Gate id: `bz_phase2_dual_projection_decision_gate`
- Dual projection plan: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_experiment_plan.md`
- Projection probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_probe.md`
- Projection rule experiment: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_rule_experiment.md`
- External calibration check: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_calibration_check.md`
- Outcome: `switch_to_external_bridge_calibration`

## Rationale

The bounded projection program succeeded as a specification exercise: it produced a stable exact packet on n<=80 and one honest retained-pair/residual split. But the first rule experiment is still bookkeeping-only and does not provide an elimination mechanism for the zeta(3) residual channel. At this point, proposing stronger projection identities would be more speculative than informative, so the next main line should fall back to the explicit external bridge path rather than invent more baseline projection rules.

## Evidence

- The shared exact baseline packet exists and is reproducible on n=1..80, with packet hash `8dde8e0e3dca2ced6b0b96eea05422f5afdf497e54e0a812c8b977a7ba9cca6a`.
- The first rule experiment produces separate retained-pair and residual-channel hashes but explicitly states that it is bookkeeping-only and does not eliminate the residual channel.
- The calibration contract from `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_calibration_check.md` has been met at the bookkeeping level, but not at the level of a published linear-form identity comparable to Zudilin 2002.

## Rejected next steps

- Do not stack more ad hoc projection rules onto the retained-pair/residual split without a new source-backed identity to test.
- Do not reopen the old n=435 dual-companion kernel engineering lane; that remains a separate deferred engineering task.
- Do not broaden literature search again before using the already-verified external bridge objects more concretely.

## Next main line

Switch to the external hypergeometric bridge path. The next artifact should specify one explicit bridge object from Zudilin 2002 or Zudilin 2018 as the first implementation-calibration target for a stronger coefficient-side comparison.
