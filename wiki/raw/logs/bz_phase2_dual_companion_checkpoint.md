# Phase 2 dual-companion checkpoint

- Status: frozen checkpoint, not the active main line.
- Baseline dual constant cache banked through `n=434`.
- Baseline dual `zeta(3)` cache banked through `n=434`.
- Latest certified dual-companion exact window: `n<=431`.
- Latest certified recurrence exclusion: shifts `(1, 0, -1, -2)` through degree `106`.
- Rank at the frontier degree: `428/428`.
- Why frozen: the remaining `n=435` step is blocked by architectural exact-arithmetic costs in the mixed fraction-pair / `mpq` kernel, while the mathematical value of one more degree step is now lower than the cost.
- Reopen criterion: Reopen only if the phase-2 pivot report finds no better repo-local proof-relevant decay path or if a true representation rewrite is explicitly prioritized.

This checkpoint preserves the exact cached dual companion data and the certified exclusion result as a reusable artifact for future representation rewrites.
