# Phase 2 dual projection experiment plan

- Plan id: `bz_phase2_dual_projection_experiment_plan`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Driving path id: `baseline_dual_projection_path`

## Rationale

The literature search is saturated enough to stop broadening it. The best remaining move is a bounded construction experiment on the dual cellular projection path, calibrated against explicit external zeta(5) bridge objects instead of waiting for a hidden published baseline P_n formula.

## Non-goals

- Do not reopen the n=435 dual-companion exact-kernel fight as the active main line.
- Do not claim a baseline P_n sequence unless the extraction path is explicit and reproducible in the repo.
- Do not widen the literature search beyond targeted bridge verification needed for implementation choices.

## Reusable assets

- Exact dual F7 constant, zeta(3), and zeta(5) coefficient extraction infrastructure.
- Frozen baseline dual-companion caches and degree-106 exclusion checkpoint.
- Totally symmetric remainder pipeline through the generic decay-probe interface.
- Construction memo in `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_construction_memo.md`.
- Literature verification report in `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_literature_verification_report.md`.
- Secondary calibration path `hypergeometric_bridge_path` with explicit external zeta(5) bridge objects.

## Milestones

### projection_target_spec

- Objective: Define one normalized target object for the first projection attempt: a baseline dual-side coefficient or linear-form component whose parity/projection meaning is explicit.
- Deliverable: A repo-native target spec and report entry that names the object, its provenance assumptions, and the exact existing caches or probes it will reuse.
- Success condition: The target object can be stated without inventing unpublished formulas and can be tied to existing baseline dual extraction code.
- Failure signal: The target cannot be formulated without hidden notation or source assumptions that are absent from the repo.

### external_calibration_check

- Objective: Use one explicit external bridge object to calibrate the projection logic before applying it to the baseline cellular family.
- Deliverable: A small calibration artifact that states which external source is used, what coefficient/projection property is being matched, and how the repo will check it.
- Success condition: The calibration target has an explicit published sequence or coefficient statement that can be compared against the repo's extraction conventions.
- Failure signal: The calibration object is too structurally different to provide a meaningful convention check.

### bounded_projection_probe

- Objective: Implement a first bounded projection probe that maps the chosen baseline dual object into a candidate decay-side summary without claiming a full baseline P_n extraction.
- Deliverable: One probe module plus one generated report that explicitly separates confirmed output, inferred output, and unresolved pieces.
- Success condition: The probe produces a stable, reproducible summary with honest missing-data flags and without reopening the old exact-kernel trench.
- Failure signal: The probe immediately requires a full representation rewrite or depends on unpublished symbolic identities.

### decision_gate

- Objective: Decide whether the bounded projection probe justifies a deeper extraction program or whether the program should fall back to the external bridge path.
- Deliverable: A short decision report that names the next main line: continue projection, switch to bridge calibration, or pause for new source material.
- Success condition: The decision is based on explicit probe output and implementation cost, not on open-ended optimism.
- Failure signal: The decision still depends mainly on source hunting or on the unresolved n=435 kernel fight.

## Stop conditions

- Stop if the first bounded projection probe requires a full exact-arithmetic representation rewrite before yielding any new baseline-side summary.
- Stop if the calibration step shows that the chosen projection conventions cannot be matched even on the external bridge object.
- Stop if the only remaining next move is speculative source hunting rather than construction work.

## Next step

Implement milestone `projection_target_spec` first, then lock one external calibration object from the hypergeometric bridge path before writing any new baseline dual projection code.
