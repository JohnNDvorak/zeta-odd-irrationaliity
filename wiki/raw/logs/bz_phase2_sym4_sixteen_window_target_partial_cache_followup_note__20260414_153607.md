# Phase 2 Sym^4 sixteen-window target partial-cache follow-up

- Date: 2026-04-14
- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic object

## Goal

Resume the target-side `Sym^4` sixteen-window construction from the current partial-cache state.

## Measured progress

- This tranche advanced from `40 / 65` to `41 / 65` windows.
- Bounded resume elapsed about `730.43` seconds.
- The cached target-side state is now at `state_window_index = 40`, `next_window_index = 41`, with lead state nonzero.
- the ordinary/rebase pattern remains:
  - completed window 35: rebase
  - completed window 36: ordinary
  - completed window 37: rebase
  - completed window 38: ordinary
  - completed window 39: rebase
  - completed window 40: ordinary
  - completed window 41: rebase
- the next predicted step is now an ordinary advancement.
