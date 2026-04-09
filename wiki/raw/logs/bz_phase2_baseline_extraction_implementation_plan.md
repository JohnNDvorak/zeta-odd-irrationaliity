# Phase 2 baseline extraction implementation plan

- Plan id: `bz_phase2_baseline_extraction_implementation_plan`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Construction memo: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_construction_memo.md`
- Path-selection memo: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_zudilin_2002_path_selection_memo.md`
- Active target object: `baseline_dual_f7_exact_coefficient_packet`

## Bridge role

Use the Zudilin 2002 bridge stack only as calibration for conventions and failure modes. Do not treat bridge-map fitting as the main line.

## Rationale

The bridge program has now supplied enough calibration: explicit comparison objects, explicit stop rules, and multiple bounded ansatz failures. The next best use of cycles is to return to baseline-side extraction with a bounded implementation plan anchored on the existing exact coefficient packet.

## Milestones

### baseline_pair_object_spec

- Objective: Freeze the exact baseline-side extraction object to be manipulated directly, starting from the baseline dual F_7 coefficient packet rather than from bridge-map surrogates.
- Deliverable: One repo-native spec naming the exact baseline extraction object, its components, and the precise output type expected from the first extraction attempt.
- Success condition: The object is stated entirely in repo-native terms and does not depend on unpublished bridge-style identities.
- Stop rule: Stop if the object spec cannot be stated without introducing hidden assumptions about baseline P_n.

### bounded_extraction_rule

- Objective: Define one bounded baseline-side extraction rule on the exact coefficient packet, with the bridge used only to sanity-check bookkeeping conventions.
- Deliverable: One extraction-rule artifact that distinguishes confirmed output, inferred structure, and unresolved remainder.
- Success condition: The rule produces a reproducible output object without reopening the old exact-kernel trench or inventing a recurrence.
- Stop rule: Stop if the rule immediately requires an unbounded symbolic rewrite or collapses back into bridge-map fitting.

### bounded_extraction_probe

- Objective: Run the first bounded extraction probe on the baseline-side object and record what, if anything, is stabilized.
- Deliverable: One generated report with explicit non-claims and a decision about whether the output is extraction-like enough to pursue.
- Success condition: The probe creates a stable repo object that is more proof-relevant than the current bridge comparison layer.
- Stop rule: Stop if the probe yields only another analog-comparison object rather than a more baseline-native extraction artifact.

### post_probe_decision_gate

- Objective: Choose whether to deepen baseline extraction, return to a narrower calibration step, or pause for a new source-backed idea.
- Deliverable: One short decision gate based on probe output and implementation cost, not on generic optimism.
- Success condition: The next line is chosen from evidence produced by the extraction probe itself.
- Stop rule: Stop if the decision still depends mainly on expanding ansatz families that the bridge memo already deprioritized.

## Non-goals

- Do not add cubic or higher bridge normalization families by default.
- Do not make the Zudilin 2002 bridge object the main target; it is calibration only.
- Do not claim baseline P_n extraction unless the new artifact is explicitly repo-native and reproducible.

## Next step

Implement `baseline_pair_object_spec` first, using the exact baseline dual F_7 coefficient packet as the active baseline-side object and the bridge stack only as a calibration boundary.
