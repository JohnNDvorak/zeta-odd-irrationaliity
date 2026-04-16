# Phase 2 autonomous directed iteration loop

- Loop id: `bz_phase2_autonomous_directed_iteration_loop`
- Scope: repo-native Brown-Zudilin `ζ(5)` research continuation
- Purpose: let a Codex operator run a bounded iteration, assess progress, make a recommendation, and then act on the recommendation without waiting for a fresh `continue` prompt
- Current frontier anchor: `Sym^4` sixteen-window higher-Schur object
- Current hard-wall anchor: constant and low-degree polynomial Sym4 matrix-recursive families are closed over their strict overdetermined ranges

## Loop states

1. `state_snapshot`
   - Read `CODEX_TRANSITION.md`, `wiki/frontier.md`, and `wiki/conclusions/exhausted-ansatz-classes.md`.
   - Run `git status --short --branch`.
   - Identify unbanked results, stale synthesis, or a single bounded research candidate.
2. `candidate_selection`
   - Prefer a genuinely different structural family over larger versions of exhausted families.
   - Require a source-backed object, an exact repo-native invariant, or a clearly stated engineering blocker.
   - Reject candidates that reopen frozen lanes or turn an overdetermined screen into interpolation.
3. `bounded_action`
   - Run one bounded computation, write one decision gate, or implement one small helper that directly enables the selected screen.
   - Avoid open-ended compute. If a run gets expensive, bank an engineering note or optimize the implementation before retrying.
4. `assessment`
   - Classify the outcome as `banked`, `hard_wall`, `promising_lead`, `engineering_wall`, `ill_posed`, or `do_not_retry`.
   - Record exact windows, witness primes, hashes, timings, and boundaries.
5. `recommendation`
   - Pick exactly one next action.
   - State why it is not a retry of an exhausted family.
   - State whether the action is auto-allowed by this loop.
6. `autonomous_action`
   - If the recommendation is auto-allowed, do it immediately.
   - If the recommendation is not auto-allowed, write a stop note and ask the user for a pivot.
7. `bank_and_push`
   - Update `data/logs/` or source files.
   - Ingest any new log into `wiki/raw/`.
   - Patch synthesis pages.
   - Rebuild index, lint, commit, and push before beginning the next iteration.

## Auto-allowed recommendations

- Bank an already-produced result.
- Add a decision gate for a completed bounded screen.
- Implement a narrowly scoped helper for a selected bounded screen.
- Run an exact or modular obstruction screen when all of these hold:
  - the object is already banked or the construction is directly source-backed
  - the family is not listed in `wiki/conclusions/exhausted-ansatz-classes.md`
  - the tested range is strictly overdetermined or otherwise has a stated structural reason
  - the expected runtime is bounded enough to monitor in one operator turn
- Patch wiki/handoff state to remove stale frontier claims.
- Commit and push cleanly scoped research artifacts.

## Not auto-allowed

- Inventing or using explicit non-symmetric baseline `P_n`.
- Reopening the exact `n=435` dual-companion lane without a new kernel architecture.
- Retrying exhausted bridge, packet, transfer, quotient, scalar, local, constant-matrix, or polynomial-matrix families by merely increasing size, order, or degree.
- Running non-overdetermined interpolation searches without a new source-backed structural reason.
- Claiming recurrence-level success from object-level success or obstruction evidence.
- Leaving a meaningful result only in chat.

## Recommendation-to-action rules

- If the result is `promising_lead`, inspect and bank the lead before trying another family.
- If the result is `hard_wall`, write or update the relevant decision gate, update exhausted classes, then select the next genuinely different candidate.
- If the result is `engineering_wall`, optimize only if the optimization directly enables the selected bounded screen; otherwise bank the wall and pivot.
- If no defensible bounded candidate exists, write a structural-selection memo and stop for user input.
- If the next action is clear and auto-allowed, start it after the commit/push for the current iteration.

## Current loop recommendation

The Sym4 constant and polynomial matrix-recursive families are exhausted over their strict overdetermined ranges. The next autonomous iteration should not increase order or degree. It should either:

- identify a genuinely different structural family on the banked Sym4 object, or
- write a structural-selection memo explaining why the next move requires user-approved mathematical direction.
