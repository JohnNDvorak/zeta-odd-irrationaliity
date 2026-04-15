# Phase 2 Sym^4 sixteen-window target partial-cache follow-up

- Date: 2026-04-14
- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic object

## Goal

Resume the target-side `Sym^4` sixteen-window construction from the previous partial-cache state.

## Measured progress

- This tranche advanced from `35 / 65` to `36 / 65` windows.
- Bounded resume elapsed about `417.41` seconds.
- The cached target-side state is now at `state_window_index = 35`, `next_window_index = 36`, with lead state `0`.
- The quartic sequence remains alternating; this step is treated as ordinary advancement, and the next step is therefore predicted to be a rebase case.
- Ordinary high-water cost rises to about `417.41` seconds; rebase high-water remains about `632.52` seconds.

## Interpretation

- The resumed cache is now `36 / 65` deep.
- The engineering bottleneck is unchanged in structure: target-side rolling updates and occasional singular-pivot rebases are still the wall.
- The next high-value engineering move remains to complete the cached run and observe if rebase frequency and cost stabilize enough for a frontier promotion.
