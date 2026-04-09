# Phase 2 construction memo

- Memo id: `bz_phase2_construction_memo`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Literature verification report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_literature_verification_report.md`
- Frozen checkpoint report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_companion_checkpoint.md`
- Readiness bridge report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_decay_bridge_report.md`
- Pivot report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_pivot_report.md`

## Executive verdict

The verified literature supports a sharp split: the totally symmetric Brown-Zudilin specialization is sequence-explicit, while the Brown-Zudilin baseline non-symmetric seed is asymptotic/arithmetic but not sequence-explicit in the checked sources. The next honest move is no longer source hunting; it is a construction program that uses the verified bridges to build a baseline decay-side extraction path.

## Banked assets

- Verified literature result: Brown-Zudilin v3 explicitly publishes the totally symmetric Brown-Zudilin specialization as a sequence-level anchor but no checked explicit baseline non-symmetric P_n / recurrence for a=(8,16,10,15,12,16,18,13).
- Frozen dual-companion checkpoint: exact baseline dual constant and zeta(3) companion caches banked through n=434 and n=434.
- Certified exclusion artifact: baseline dual companion sequences have no nontrivial (1,0,-1,-2) polynomial recurrence through degree 106 on the exact window n<=431.
- Repo-native calibration anchor: the totally symmetric remainder pipeline is source-backed, normalized through the generic decay-probe interface, and currently verified through n=14.
- Bridge literature: explicit external zeta(5) linear-form constructions exist in Zudilin 2002 and Zudilin 2018, plus denominator-side cellular and motivic/parity bridges in McCarthy-Osburn-Straub 2020, Dupont 2018, and Tosi 2026.

## Missing objects

- No checked explicit baseline non-symmetric P_n sequence for a=(8,16,10,15,12,16,18,13).
- No checked explicit baseline non-symmetric recurrence analogous to the symmetric Section 2 recurrence.
- No checked direct baseline remainder fixture that can be ingested into the generic decay-probe pipeline.

## Construction paths

### Dual cellular projection path

- Path id: `baseline_dual_projection_path`
- Objective: Turn the Brown-Zudilin generalized baseline family itself into explicit coefficient data by combining the dual-cellular perspective with a coefficient/parity projection mechanism.
- Supporting sources: `Brown-Zudilin, arXiv:2210.03391v3`, `Brown, Irrationality proofs, moduli spaces and dinner parties (2014 notes)`, `Dupont, Odd zeta motive and linear forms in odd zeta values (2018)`
- Existing assets: `Exact dual F7 coefficient extraction infrastructure in the repo.` `Frozen dual companion caches and exclusion report.` `Generic decay-probe and baseline readiness-bridge reports.`
- Blocking gap: No published coefficient-extraction algorithm specialized to the Brown-Zudilin baseline seed; the projection step must be constructed rather than ingested.
- Payoff: Highest proof relevance, because success would produce a baseline-family decay object instead of an external analog.
- Risk: High mathematical and engineering risk: this is a new extraction build, not a simple transcription of a published recurrence.
- Recommendation: Primary construction path once we stop expecting a hidden published baseline P_n formula to appear.

### External hypergeometric bridge comparison path

- Path id: `hypergeometric_bridge_path`
- Objective: Use explicit external zeta(5) linear-form constructions as calibration and comparison targets to infer what kind of coefficient structure the baseline cellular side would need to expose.
- Supporting sources: `Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)`, `Zudilin, Arithmetic of linear forms involving odd zeta values (2002)`, `Zudilin, Some hypergeometric integrals for linear forms in zeta values (2018)`
- Existing assets: `Verified literature report already identifies these as explicit external decay-side bridge objects.` `Repo has exact dual-side coefficient extraction machinery and sequence identity infrastructure.`
- Blocking gap: This path does not directly solve the Brown-Zudilin baseline problem; it only constrains or suggests candidate extraction shapes.
- Payoff: Moderate payoff with lower risk: it can sharpen target invariants and provide implementation tests without first solving the full baseline projection problem.
- Risk: Risk of overfitting to neighboring zeta(5) constructions that are structurally different from the generalized cellular baseline.
- Recommendation: Best secondary path and the safest place to prototype extraction logic before applying it to the baseline family.

### Generalized cellular contiguity / denominator-side reconstruction path

- Path id: `cellular_contiguity_path`
- Objective: Reconstruct explicit baseline coefficient data from the generalized cellular family using the baseline matrix, denominator-side cellular analogs, and any recoverable contiguity structure.
- Supporting sources: `Brown-Zudilin, arXiv:2210.03391v3`, `McCarthy-Osburn-Straub, Sequences, modular forms and cellular integrals (2020)`, `Tosi, An explicit study of a family of cellular integrals (2026)`, `Tosi, dissertation / reflection-arrangement framework (2026)`
- Existing assets: `Repo has baseline Q_n infrastructure, modular recurrence scanners, and the verified baseline matrix reference.` `Literature report now separates basic-cellular denominator-side results from the missing generalized baseline decay object.`
- Blocking gap: No checked published contiguity package for the generalized non-symmetric baseline seed; the needed coefficient-recovery mechanism is still implicit.
- Payoff: Potentially high if a workable contiguity relation is found, because it would stay closest to the actual Brown-Zudilin baseline family.
- Risk: High risk of large symbolic complexity and of reproducing the same exact-arithmetic bottlenecks in a new guise.
- Recommendation: Promising only after the literature-backed projection and bridge routes are clearly exhausted or better specified.

## Recommended next step

Treat the literature search as saturated enough to stop broadening it. Keep the current baseline readiness bridge (`bz_phase2_baseline_decay_readiness_bridge`) and pivot outcome (`build_baseline_decay_readiness_bridge`), then begin a bounded construction program on the dual cellular projection path, using the external hypergeometric bridge path as calibration.
