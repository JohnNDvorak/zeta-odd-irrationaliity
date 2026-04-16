# Codex Transition

Status snapshot for a fresh Codex resuming this repo.

- Date: `2026-04-16`
- Repo: `zeta5-autoresearch`
- Current pushed commit before this update: `9d8523f`
- Strongest banked mathematical frontier: `Sym^4` sixteen-window higher-Schur object
- Live follow-up subfrontier: exact nullspace follow-up on three target-side generalized polynomial matrix cases
- Frozen exact-side frontier: dual companion caches through `n=434`; no nontrivial `(1,0,-1,-2)` polynomial recurrence through degree `106` on certified window `n<=431`

## Read This First

Start in this order:

1. `README.md`
2. `CODEX_TRANSITION.md`
3. `WIKI_OPERATIONS.md`
4. `wiki/frontier.md`
5. `wiki/concepts/autonomous-directed-iteration-loop.md`
6. `wiki/audits/completed-directions.md`
7. `wiki/conclusions/exhausted-ansatz-classes.md`
8. `wiki/computation/exact-side-frozen-frontier.md`
9. `wiki/computation/sym4-sixteen-window-frontier.md`
10. `wiki/computation/sym3-eleven-window-frontier.md`
11. `wiki/audits/sym4-sixteen-window-compute-wall.md`
12. `wiki/audits/sym4-sixteen-window-target-partial-cache-progress.md`

Do not start by rereading the whole repo or re-deriving early program history. The wiki already banks that work.

## Program Goal

The program goal is still the same:

- prove irrationality of `ζ(5)` by finding an Apéry-type exact arithmetic object, or an exact/source-backed surrogate strong enough to lead there;
- stay within the Brown-Zudilin `M_{0,8}` cellular framework unless there is a clear, source-backed reason to leave it;
- prefer exact arithmetic and source-backed objects over heuristic numerics.

The practical working objective is narrower:

- build or extract exact objects that might support a useful recurrence-level or linear-form structure;
- certify hard walls honestly when a family fails;
- preserve enough provenance that the repo is cumulative rather than repetitive.

## What This Project Actually Became

This repo started as a direct exact-sequence and recurrence search around Brown-Zudilin baseline and dual objects.

That lane hit a real wall:

- the dual companion exact cache was pushed to `n=434`;
- the natural cleared-window `(1,0,-1,-2)` polynomial recurrence family was ruled out through degree `106` on `n<=431`;
- six rounds of kernel engineering still did not make the `n=435` step viable enough to justify continuing the same lane blindly.

That forced a phase-2 pivot:

- stop pretending the exact `n=435` fight was one micro-optimization away from success;
- move to source-backed decay-side objects, transfer experiments, packet objects, and nonlinear invariants;
- treat every new lane as a bounded experiment with an explicit decision gate.

The live repo now has three layers:

1. A frozen exact-side obstruction program.
2. A banked nonlinear object ladder now culminating in `Sym^4` sixteen-window.
3. A recurrence-screen follow-up on the banked quartic object, with natural monic matrix families closed and a non-monic polynomial matrix lead now promoted to exact-nullspace extraction.

## Core Methodology

The project now operates under the following discipline.

### 1. Exact arithmetic is load-bearing

- Exact rational arithmetic is the default.
- Modular inconsistency screens are allowed when used honestly as obstruction evidence.
- Numerical agreement is never treated as certification.

### 2. Source-backed means source-backed

- The explicit non-symmetric baseline `P_n` is not source-backed in the checked Brown-Zudilin neighborhood.
- Never behave as if baseline `P_n` is known.
- The totally symmetric decay-side triple is source-backed and safe to use as an anchor.

### 3. Every lane ends in a banked artifact

Every substantive experiment should end as one of:

- `banked`
- `hard wall`
- `frozen`
- `engineering progress`
- `current frontier`
- `ill-posed`
- `do not retry`

If a lane stalls, write the decision gate and move on. Do not leave half-proven intuitions in chat only.

### 4. Prefer genuinely different object classes

The program has already exhausted many “same shape, slightly bigger” moves. New work should usually mean one of:

- a genuinely different nonlinear invariant;
- a materially different recurrence family;
- a source-backed bridge with new structural justification;
- or an engineering change that addresses a demonstrated computational wall directly.

### 5. Separate mathematical frontier from engineering frontier

This distinction matters:

- `Sym^4` sixteen-window is the strongest banked mathematical object.
- Its homogeneous recurrence screen is banked as a hard wall through order `4`; do not claim a recurrence-level success from that obstruction.
- Its affine recurrence screen is banked as a hard wall through order `3`; do not claim a recurrence-level success from that obstruction.

Advertise the quartic lane only at the level that is banked: object-level success, two constant matrix-ladder obstructions, and a low-degree monic polynomial matrix obstruction are real; the non-monic target-side cases are exact-nullspace follow-up leads, not recurrence successes.

### 6. Run the autonomous directed loop

When the user says `continue`, run the [[autonomous-directed-iteration-loop]] rather than stopping at a recommendation:

1. Snapshot the frontier, exhausted-family ledger, and git state.
2. Select exactly one bounded candidate.
3. Run the bounded action.
4. Assess the result as `banked`, `hard_wall`, `promising_lead`, `engineering_wall`, `ill_posed`, or `do_not_retry`.
5. Recommend exactly one next action.
6. If the recommendation is auto-allowed by the loop, act on it immediately.
7. Bank, ingest, patch synthesis pages, rebuild index, lint, commit, and push before the next iteration.

Stop only when the next step violates a guardrail, needs user mathematical judgment, or would become an unbounded/interpolation search.

## Current Frontier

### Frozen exact-side frontier

- Dual companion caches are banked through `n=434`.
- No nontrivial `(1,0,-1,-2)` polynomial recurrence exists through degree `106`.
- Certified exact obstruction window: `n<=431`.
- This lane is frozen. Reopen it only with a genuinely new kernel architecture, not with another parameter tweak.

Primary files:

- `src/zeta5_autoresearch/bz_dual_f7.py`
- `src/zeta5_autoresearch/dual_f7_exact_coefficient_cache.py`
- `src/zeta5_autoresearch/bz_dual_f7_companion_normalization_probe.py`
- `wiki/computation/exact-side-frozen-frontier.md`

### Strongest banked mathematical object

The strongest banked object is the `Sym^4` sixteen-window higher-Schur invariant.

Banked facts:

- exact paired object on `n=1..65`
- coordinate count `15`
- source hash `fc9ceb94cfd7c56b98d3f69c2a3efb4e7e47020e3fd1a8be628bf173d9dd476e`
- target hash `216eede544444133c25cd8b82e1b83b991f54d3183c347f2351aed29dbedfc09`
- paired object hash `dfe18fe136e64e09be99280cd26919bb5e28219f81847e73d7dbfca7ee85b606`
- final target sequence cache materialized at `data/cache/bz_phase2_sym4_sixteen_window_target_sequence_cache.json`
- homogeneous matrix ladder through order `4` is closed on source and target
- affine matrix ladder through order `3` is closed on source and target
- low-degree polynomial matrix recurrence screen is closed over every strict overdetermined tested case:
  - homogeneous `(order, degree) = (1,1)`, `(1,2)`, `(1,3)`, and `(2,1)`
  - affine `(order, degree) = (1,1)`, `(1,2)`, and `(2,1)`
- generalized non-monic polynomial matrix recurrence screen has three target-side exact-nullspace follow-up cases:
  - homogeneous `(order, degree) = (1,2)`
  - homogeneous `(order, degree) = (1,3)`
  - affine `(order, degree) = (1,2)`
- bounded follow-up over primes `1451`, `1009`, `1453`, `1459`, `1471`, `1481`, `1483`, `1487`, `1489`, and `1493` found persistent modular nullity at every good target prime tested
- target reductions at primes `1009` and `1459` were denominator-singular

Primary files:

- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_object_spec.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_probe.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_matrix_recurrence_screen.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_affine_matrix_recurrence_screen.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_polynomial_matrix_recurrence_screen.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_generalized_polynomial_matrix_followup.py`
- `wiki/computation/sym4-sixteen-window-frontier.md`

### Live recurrence-screen subfrontier

The active continuation is now the recurrence-screen follow-up on the banked quartic `Sym^4` sixteen-window object.

What is established:

- source side is tractable:
  - `_build_sym4_sixteen_window_side("source")` improved from about `6.443s` to about `2.990s` under the GMP-backed rolling rewrite
- target-side all-or-nothing construction was the blocker, but the persisted cache reached `65 / 65`
- target-side initialization is about `103.23s`
- exact cached target-side progress is now `65 / 65`
- the final target sequence cache is materialized and about `131.7 MB`
- default cache loading needed one code fix: fraction deserialization now uses the repo's digit-guard-safe parser
- the generated Sym4 probe report establishes the paired object and its hashes

Current interpretation:

- target-cache construction is no longer the active blocker;
- `Sym^4` is banked at the object level;
- the next question is exact nullspace extraction/certification on the three generalized target-side cases; do not switch families before assessing those leads.

Primary files:

- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_object_spec.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_probe.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_generalized_polynomial_matrix_followup.py`
- `wiki/audits/sym4-sixteen-window-compute-wall.md`
- `wiki/audits/sym4-sixteen-window-target-partial-cache-progress.md`
- `wiki/audits/sym4-sixteen-window-generalized-polynomial-matrix-followup.md`
- `wiki/computation/sym4-sixteen-window-frontier.md`

## Closed-Off or Frozen Lanes

These are the important “do not casually retry” results.

### Exact-side

- Do not retry the old `n=435` dual companion extension without a new architecture.
- The existing mixed fraction-pair / `mpq` line already consumed six kernel redesigns.

### Baseline recurrence lane

- Low-order / low-degree baseline recurrence families have been surveyed extensively.
- This is not the place to burn time absent a new structural reason.

### Zudilin 2002 bridge lane

Exhausted bridge ansatz classes:

- scalar normalization map
- affine normalization map
- quadratic normalization map
- coupled-channel constant `2x2` map

The Zudilin 2002 object remains a calibration anchor, not a direct proof ingredient.

### Packet extraction lane

Exhausted packet choices:

- `(const, ζ(5))` with `ζ(3)` residual
- `(ζ(5), ζ(3))` with constant residual
- full `(const, ζ(3), ζ(5))` packet

All hit the same bounded refinement ladder.

### Transfer lane

Exhausted transfer families:

- symmetric to baseline
- symmetric dual to baseline dual
- annihilator-profile transfer
- symmetric source packet compression

All stall in the same bounded refinement pattern.

### Quotient variants

Weaker than normalized invariants:

- projective quotient Plücker families
- cross-ratio quotient Plücker families

Do not retry quotient variants without a very explicit reason why they escape the already observed weakness pattern.

### Low-order matrix ladders already closed

These are banked obstruction results, not open invitations:

- six-window normalized Plücker:
  - low-order constant matrix families closed through last overdetermined order
  - low-order global shared-scalar vector recurrences closed
  - short local-annihilator families closed
- seven-window normalized Plücker:
  - homogeneous constant-matrix order `1..2` closed
  - affine constant-matrix order `1..2` closed
- eight-window normalized Plücker:
  - overdetermined constant-matrix order `1` closed
- `Sym^2` seven-window:
  - homogeneous order `1..10` closed
  - affine order `1..10` closed
- `Sym^2` eight-window:
  - homogeneous order `1..2` closed
  - affine order `1..2` closed
- `Sym^3` eleven-window:
  - homogeneous order `1..6` closed
  - affine order `1..6` closed
- `Sym^4` sixteen-window:
  - homogeneous order `1..4` closed
  - affine order `1..3` closed
  - matrix-ladder decision gate banked; do not escalate matrix order mechanically
  - low-degree polynomial matrix cases closed over the strict overdetermined range; do not escalate polynomial degree mechanically

## High-Level Direction History

This is the compact research narrative a new Codex needs.

### Directions 1–6: phase-1 exact lane

1. Repo scaffolding and exact workflow: banked.
2. Baseline `Q_n` study: banked.
3. Baseline low-complexity recurrence obstruction: hard wall.
4. Dual `F_7` exact extraction: banked.
5. Dual companion recurrence obstruction through degree `106`: hard wall.
6. Kernel-engineering marathon for `n=435`: frozen wall.

### Directions 7–13: phase-2 pivot

7. Phase-2 pivot and decay audit: banked.
8. Literature verification and construction memo: banked.
9. Zudilin 2002 bridge stack: hard wall.
10. Baseline extraction on multiple packet choices: hard wall.
11. Symmetric source packet compression: hard wall.
12. Transfer-object ladder: hard wall.
13. Nonlinear object ladder: this label now covers the beyond-Plücker progression that followed.

### Post-pivot nonlinear ladder inside direction 13

This is where the live frontier actually moved:

- six-window normalized Plücker: banked predecessor object; first nonlinear improvement
- seven-window normalized Plücker: banked predecessor object
- eight-window normalized Plücker: banked predecessor object
- `Sym^2` seven-window normalized maximal-minor: banked
- `Sym^2` eight-window continuation: banked
- `Sym^3` eleven-window higher-Schur: strongest predecessor with banked hard-wall screens
- `Sym^4` sixteen-window: strongest banked mathematical object; monic constant and low-degree polynomial matrix screens closed through their strict overdetermined ranges; generalized non-monic polynomial matrix screen has three target-side exact-follow-up cases

The important subtlety is that `wiki/audits/completed-directions.md` still treats these later objects as part of direction `13`. That is intentional. Do not mistake it for missing bookkeeping.

## Important Repo Areas

### Root docs

- `README.md`: public-facing repo summary
- `PROGRAM_FOR_CODEX.md`: historical bootstrapping memo; useful for origin, but stale as an operational handoff
- `CODEX_TRANSITION.md`: current operator handoff
- `WIKI_OPERATIONS.md`: procedural wiki ingest / update / lint guide

### Core code

- `src/zeta5_autoresearch/bz_dual_f7.py`: exact extractor and the most important old-kernel file
- `src/zeta5_autoresearch/dual_packet_window_plucker.py`: core nonlinear window geometry support
- `src/zeta5_autoresearch/dual_packet_schur_functor.py`: higher-Schur lift support
- `src/zeta5_autoresearch/wiki_cli.py`: wiki ingest / lint / index support

### Logs and cache

- `data/logs/`: mutable working artifacts, reports, decision gates, checkpoint notes
- `data/cache/`: exact cached data, including the quartic target cache

### Wiki

- `wiki/raw/`: immutable snapshots for citation
- `wiki/`: synthesized pages maintained by the agent
- `wiki/index.md`: content catalog
- `wiki/log.md`: append-only operational log

## Knowledge Wiki Contract

The full procedural version of this section lives in `WIKI_OPERATIONS.md`. This section is the short strategic version.

The wiki is the cumulative memory layer. Use it like this.

### Invariants

- `wiki/raw/` is immutable and citeable.
- `wiki/` is synthetic and maintained by the agent.
- The wiki should cite `wiki/raw/*` snapshots, not live `data/logs/*` files.
- The repo can still read and edit `src/` and `data/logs/` for actual work; the “do not read from data/logs directly” rule applies to wiki citation discipline, not to coding.

### Query workflow

When resuming or answering substantive questions:

1. Read `wiki/index.md`.
2. Read `wiki/frontier.md`.
3. Read the relevant object, conclusion, and audit pages.
4. Check `wiki/conclusions/exhausted-ansatz-classes.md` before suggesting a new family.

### Ingest workflow

For a new document in `data/logs/`:

1. Make sure the log file is correct.
2. Ingest it:

```bash
uv run python -m zeta5_autoresearch.wiki_cli ingest data/logs/<filename>.md
```

3. Find the newest raw snapshot:

```bash
ls -1t wiki/raw/logs/<stem>* | head -3
```

4. Patch the relevant synthesis pages manually.

Typical targets:

- `wiki/frontier.md`
- the specific audit page for the object or screen
- sometimes a computation page
- sometimes a conclusion page

5. Rebuild the index:

```bash
uv run python - <<'PY'
from pathlib import Path
from zeta5_autoresearch.wiki_cli import build_index
build_index(Path('.').resolve())
PY
```

6. Lint the wiki:

```bash
uv run python -m zeta5_autoresearch.wiki_cli lint
```

7. Commit and push.

### Canonical wiki pages for resumption

These are the most important current pages:

- `wiki/frontier.md`
- `wiki/audits/completed-directions.md`
- `wiki/conclusions/exhausted-ansatz-classes.md`
- `wiki/computation/exact-side-frozen-frontier.md`
- `wiki/computation/sym3-eleven-window-frontier.md`
- `wiki/audits/sym4-sixteen-window-compute-wall.md`
- `wiki/audits/sym4-sixteen-window-target-partial-cache-progress.md`
- `wiki/literature/brown-zudilin-2210-03391v3.md`
- `wiki/literature/zudilin-2002.md`

## Canonical Documents

If a fresh Codex is rebuilding context or restoring the wiki from scratch, these are the first documents to ingest or reread.

### Phase-1 exact core

- `data/logs/bz_baseline_recurrence_report.md`
- `data/logs/bz_baseline_modular_family_survey_report.md`
- `data/logs/bz_baseline_shift_catalog_survey_report.md`
- `data/logs/bz_dual_f7_exact_probe_report.md`
- `data/logs/bz_dual_f7_probe_report.md`
- `data/logs/bz_dual_f7_companion_normalization_report.md`
- `data/logs/bz_phase2_dual_companion_checkpoint.md`

### Phase-2 pivot and literature

- `data/logs/bz_phase2_pivot_report.md`
- `data/logs/bz_phase2_baseline_decay_audit_report.md`
- `data/logs/bz_phase2_baseline_decay_bridge_report.md`
- `data/logs/bz_phase2_literature_verification_report.md`
- `data/logs/bz_phase2_construction_memo.md`

### Nonlinear and higher-Schur lineage

- `data/logs/bz_phase2_normalized_plucker_window_invariant_screen.md`
- `data/logs/bz_phase2_plucker_quotient_family_screen.md`
- `data/logs/bz_phase2_six_window_plucker_followup_screen.md`
- `data/logs/bz_phase2_seven_window_normalized_plucker_decision_gate.md`
- `data/logs/bz_phase2_eight_window_normalized_plucker_decision_gate.md`
- `data/logs/bz_phase2_sym2_seven_window_affine_decision_gate.md`
- `data/logs/bz_phase2_sym2_eight_window_affine_decision_gate.md`
- `data/logs/bz_phase2_sym3_eleven_window_affine_decision_gate.md`

### Quartic engineering frontier

- `data/logs/bz_phase2_sym4_sixteen_window_compute_wall_note.md`
- `data/logs/bz_phase2_sym4_sixteen_window_engineering_followup_note.md`
- `data/logs/bz_phase2_sym4_sixteen_window_gmp_followup_note.md`
- `data/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note.md`

### Literature-side refs already mirrored into the wiki

- `refs/notes_brown_2014.md`
- `refs/notes_bz_2026.md`
- `refs/notes_dupont_2018.md`
- `refs/notes_tosi_2026.md`

## Standard Commands

### Run regressions

```bash
uv run pytest
```

### Inspect quartic target cache state

```bash
python - <<'PY'
from pathlib import Path
import json
p = Path('data/cache/bz_phase2_sym4_sixteen_window_target_partial_cache.json')
payload = json.loads(p.read_text())
print('completed', payload['completed_window_count'])
print('next', payload['next_window_index'])
print('state', payload.get('state_window_index'))
print('lead_is_zero', payload['coordinate_numerators'][0] == '0')
PY
```

### Advance quartic target cache by one bounded window

This is now mostly historical. The target cache has reached `65 / 65`; use it only if validating or rebuilding cache state intentionally.

```bash
uv run python -u - <<'PY'
from time import perf_counter
from zeta5_autoresearch.symmetric_dual_baseline_sym4_sixteen_window_probe import (
    resume_sym4_sixteen_window_target_partial_cache,
)
start = perf_counter()
progress = resume_sym4_sixteen_window_target_partial_cache(
    max_runtime_seconds=420.0,
    max_windows_per_run=1,
)
print(progress)
print('elapsed', perf_counter() - start)
PY
```

Tune `max_runtime_seconds` to the predicted branch:

- ordinary branch: about `260-320s` is usually enough
- rebase branch: about `380-420s` is safer

### Wiki maintenance

```bash
uv run python -m zeta5_autoresearch.wiki_cli ingest data/logs/<filename>.md
uv run python -m zeta5_autoresearch.wiki_cli lint
```

## Resume Protocol

When a fresh Codex takes over, do this first:

1. Read the files in the “Read This First” section.
2. Run `git status --short`.
3. Ignore the two long-lived untracked regression drafts unless you intentionally want them:
   - `regression/test_symmetric_dual_baseline_sym4_sixteen_window.py`
   - `regression/test_symmetric_dual_baseline_sym4_sixteen_window_affine.py`
4. Run the autonomous directed loop from `wiki/concepts/autonomous-directed-iteration-loop.md`.
5. Check the quartic cache state only if the selected loop action depends on cache validity.
6. Continue the loop-selected branch only if there is no new analytic blocker.
7. After each meaningful result:
   - update the relevant `data/logs/*.md` note
   - ingest it into the wiki
   - patch synthesis pages
   - rebuild index
   - run wiki lint
   - commit and push

## What Not To Do

- Do not invent baseline non-symmetric `P_n`.
- Do not reopen the old `n=435` lane without a new kernel architecture.
- Do not retry exhausted bridge, packet, transfer, quotient, or low-order matrix families without a fresh structural reason.
- Do not confuse an engineering cache milestone with a banked mathematical object.
- Do not leave substantive conclusions only in chat; write the artifact and update the wiki.

## Immediate Next Move

Use the autonomous directed loop. The current state it must respect is: the natural monic Sym4 matrix families are banked as hard walls:

- homogeneous matrix ladder through order `4`
- affine matrix ladder through order `3`
- low-degree polynomial matrix extension over every strict overdetermined tested case
- source and target separately
- decision gate: `bz_phase2_sym4_sixteen_window_matrix_ladder_decision_gate`

The next loop-selected action is exact follow-up on the generalized non-monic target-side cases:

- homogeneous `(order, degree) = (1,2)`
- homogeneous `(order, degree) = (1,3)`
- affine `(order, degree) = (1,2)`

Decision rule:

- choose another lane only with a genuinely different structural reason;
- do not retry bridge, packet, transfer, quotient, scalar, or order-escalated matrix families without that reason;
- do not claim baseline `P_n` extraction or reopen exact `n=435` from the object-level success alone.
