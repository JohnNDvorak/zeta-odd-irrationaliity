# Phase 2 Sym^4 sixteen-window target partial-cache follow-up

- Date: 2026-04-14
- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic object

## Goal

Turn the target-side `Sym^4` sixteen-window construction from an all-or-nothing exact build into a resumable cached pipeline.

## What changed

- Added a persisted target-side partial cache path in the draft quartic probe.
- The target-side cache now stores:
  - rolling common-denominator inverse-row state
  - rolling coordinate numerators
  - already recovered exact profile vectors
- The cache is now written immediately after initialization, so long runs bank usable state even before the first completed profile is emitted.
- Resume now supports bounded runs via `max_windows_per_run`.

## Initialization timing

Direct timing of the quartic target-side initialization split the cost as follows:

- target packet load: approximately `1.56s`
- quartic lift: approximately `0.18s`
- integerization: approximately `0.43s`
- initial basis inverse: approximately `92.53s`
- common-denominator row encoding: approximately `8.51s`
- initial coordinate extraction: approximately `0.02s`
- total initialization: approximately `103.23s`

This shows the first cache write is dominated by the initial quartic target-side basis inverse.

## Cache progress

The new target-side partial cache is real and persisted:

- cache file: `data/cache/bz_phase2_sym4_sixteen_window_target_partial_cache.json`
- current exact progress reached during this tranche: `61 / 65` windows

Measured bounded resumes:

- first long resume reached the first persisted profile:
  - progress `1 / 65`
- second bounded resume:
  - progress `2 / 65`
  - elapsed approximately `73.19s`
- third bounded resume required a singular-pivot recovery step:
  - progress `3 / 65`
  - elapsed approximately `140.81s`
- fourth bounded resume on a nonsingular step:
  - progress `4 / 65`
  - elapsed approximately `84.06s`
- fifth bounded resume required another singular-pivot recovery step:
  - progress `5 / 65`
  - elapsed approximately `154.61s`
- sixth bounded resume on a nonsingular step:
  - progress `6 / 65`
  - elapsed approximately `93.39s`
- seventh bounded resume required another singular-pivot recovery step:
  - progress `7 / 65`
  - elapsed approximately `188.13s`
- eighth bounded resume on a nonsingular step:
  - progress `8 / 65`
  - elapsed approximately `111.81s`
- ninth bounded resume required another singular-pivot recovery step:
  - progress `9 / 65`
  - elapsed approximately `221.46s`
- tenth bounded resume on a nonsingular step:
  - progress `10 / 65`
  - elapsed approximately `124.94s`
- eleventh bounded resume required another singular-pivot recovery step:
  - progress `11 / 65`
  - elapsed approximately `238.43s`
- twelfth bounded resume on a nonsingular step:
  - progress `12 / 65`
  - elapsed approximately `136.17s`
- thirteenth bounded resume required another singular-pivot recovery step:
  - progress `13 / 65`
  - elapsed approximately `254.55s`
- fourteenth bounded resume on a nonsingular step:
  - progress `14 / 65`
  - elapsed approximately `160.05s`
- fifteenth bounded resume required another singular-pivot recovery step:
  - progress `15 / 65`
  - elapsed approximately `265.43s`
- sixteenth bounded resume on a nonsingular step:
  - progress `16 / 65`
  - elapsed approximately `166.79s`
- seventeenth bounded resume required another singular-pivot recovery step:
  - progress `17 / 65`
  - elapsed approximately `306.43s`
- eighteenth bounded resume on a nonsingular step:
  - progress `18 / 65`
  - elapsed approximately `191.74s`
- nineteenth bounded resume required another singular-pivot recovery step:
  - progress `19 / 65`
  - elapsed approximately `320.45s`
- twentieth bounded resume on a nonsingular step:
  - progress `20 / 65`
  - elapsed approximately `202.42s`
- twenty-first bounded resume required another singular-pivot recovery step:
  - progress `21 / 65`
  - elapsed approximately `359.54s`
- twenty-second bounded resume on a nonsingular step:
  - progress `22 / 65`
  - elapsed approximately `230.96s`
- twenty-third bounded resume required another singular-pivot recovery step:
  - progress `23 / 65`
  - elapsed approximately `381.81s`
- twenty-fourth bounded resume on a nonsingular step:
  - progress `24 / 65`
  - elapsed approximately `251.87s`
- twenty-fifth bounded resume required another singular-pivot recovery step:
  - progress `25 / 65`
  - elapsed approximately `418.63s`
- twenty-sixth bounded resume on a nonsingular step:
  - progress `26 / 65`
  - elapsed approximately `272.83s`
- twenty-seventh bounded resume required another singular-pivot recovery step:
  - progress `27 / 65`
  - elapsed approximately `458.46s`
- twenty-eighth bounded resume on a nonsingular step:
  - progress `28 / 65`
  - elapsed approximately `299.93s`
- twenty-ninth bounded resume required another singular-pivot recovery step:
  - progress `29 / 65`
  - elapsed approximately `477.21s`
- thirtieth bounded resume on a nonsingular step:
  - progress `30 / 65`
  - elapsed approximately `293.86s`
- thirty-first bounded resume required another singular-pivot recovery step:
  - progress `31 / 65`
  - elapsed approximately `512.50s`
- thirty-second bounded resume on a nonsingular step:
  - progress `32 / 65`
  - elapsed approximately `340.60s`
- thirty-third bounded resume required another singular-pivot recovery step:
  - progress `33 / 65`
  - elapsed approximately `584.00s`
- thirty-fourth bounded resume required another rebased state alignment plus profile write:
  - progress `35 / 65`
  - elapsed approximately `632.52s`

## New obstruction uncovered

The cache work exposed a structural issue in the rolling quartic target-side path:

- after the second completed window, the cached rolling state had `coordinates[0] = 0`
- this makes the naive codimension-one rolling shift singular at that window
- without intervention, the resumed target-side cache would fail when trying to align to the next window

## Recovery step added

To keep the cached target-side path viable, the quartic resume logic now performs a controlled rebase:

- if the rolling lead coordinate is zero, rebuild the common-denominator inverse-row state directly from the next window basis
- continue the cached run from that rebased state instead of treating the singular pivot as fatal

This turned the singular-pivot event from a hard failure into an expensive but recoverable step.

The current cached state after the sixth completed window again had `coordinates[0] = 0`, so the seventh bounded resume required another rebase. After the seventh completed window, the cached lead became nonzero again. After the eighth completed window, the cached lead returned to zero again, so the ninth bounded resume required another rebase. After the ninth completed window, the cached lead became nonzero again. After the tenth completed window, the cached lead returned to zero again, so the eleventh bounded resume required another rebase. After the eleventh completed window, the cached lead became nonzero again. After the twelfth completed window, the cached lead returned to zero again, so the thirteenth bounded resume required another rebase. After the thirteenth completed window, the cached lead became nonzero again. After the fourteenth completed window, the cached lead returned to zero again, so the fifteenth bounded resume required another rebase. After the fifteenth completed window, the cached lead became nonzero again. After the sixteenth completed window, the cached lead returned to zero again, so the seventeenth bounded resume required another rebase. After the seventeenth completed window, the cached lead became nonzero again. After the eighteenth completed window, the cached lead returned to zero again, so the nineteenth bounded resume required another rebase. After the nineteenth completed window, the cached lead became nonzero again. After the twentieth completed window, the cached lead returned to zero again, so the twenty-first bounded resume required another rebase. After the twenty-first completed window, the cached lead became nonzero again. After the twenty-second completed window, the cached lead returned to zero again, so the twenty-third bounded resume required another rebase. After the twenty-third completed window, the cached lead became nonzero again. After the twenty-fourth completed window, the cached lead returned to zero again, so the twenty-fifth bounded resume required another rebase. After the twenty-fifth completed window, the cached lead became nonzero again. After the twenty-sixth completed window, the cached lead returned to zero again, so the twenty-seventh bounded resume required another rebase. After the twenty-seventh completed window, the cached lead became nonzero again. After the twenty-eighth completed window, the cached lead returned to zero again, so the twenty-ninth bounded resume required another rebase. After the twenty-ninth completed window, the cached lead became nonzero again. After the thirtieth completed window, the cached lead returned to zero again, so the thirty-first bounded resume required another rebase. After the thirty-first completed window, the cached lead became nonzero again. After the thirty-second completed window, the cached lead returned to zero again. After the thirty-third completed window, which required a rebase, the cached lead became nonzero again. After the thirty-fifth completed window, which required pre-step rebase alignment from state `34 / 33`, the cached lead remained nonzero. Through the first thirty-five completed windows, the quartic target-side cache has therefore continued to exhibit an alternating pattern between nonsingular ordinary advances and singular-pivot recovery steps.

## Current interpretation

- checkpointed rolling-state reuse is now viable for the quartic target side
- persisted partial target-side window caches are now real, not hypothetical
- however, the target-side `Sym^4` path is still expensive enough that it is not yet a banked frontier object
- the remaining wall is no longer “cannot checkpoint”
- the remaining wall is:
  - very expensive initial quartic target-side inverse
  - expensive ordinary resumed advances
  - occasional even more expensive singular-pivot rebases
- the seventeenth completed window is the first rebase case to break above the previous high-water mark, landing at approximately `306.43s`
- the eighteenth completed window is likewise the first ordinary case to break above the previous high-water mark, landing at approximately `191.74s`
- the twentieth completed window lifts the ordinary high-water mark again, to approximately `202.42s`
- the twenty-first completed window lifts the rebase high-water mark again, to approximately `359.54s`
- the twenty-second completed window lifts the ordinary high-water mark again, to approximately `230.96s`
- the twenty-third completed window lifts the rebase high-water mark again, to approximately `381.81s`
- the twenty-fourth completed window lifts the ordinary high-water mark again, to approximately `251.87s`
- the twenty-fifth completed window lifts the rebase high-water mark again, to approximately `418.63s`
- the twenty-sixth completed window lifts the ordinary high-water mark again, to approximately `272.83s`
- the twenty-seventh completed window lifts the rebase high-water mark again, to approximately `458.46s`
- the twenty-eighth completed window lifts the ordinary high-water mark again, to approximately `299.93s`
- the twenty-ninth completed window lifts the rebase high-water mark again, to approximately `477.21s`
- the thirtieth completed window was another ordinary advance, landing below the current ordinary high-water mark at approximately `293.86s`
- the thirty-first completed window lifts the rebase high-water mark again, to approximately `512.50s`
- the thirty-second completed window lifts the ordinary high-water mark again, to approximately `340.60s`
- the thirty-third completed window lifts the rebase high-water mark again, to approximately `584.00s`
- the thirty-fifth completed window lifts the rebase high-water mark again, to approximately `632.52s`

## Recommendation

The next engineering move should not be another tiny solver tweak. The strongest follow-up is:

- continue the cached quartic target-side build with the new rebase-capable resume path
- bank progress measurements and singular-pivot frequency
- only then decide whether quartic is maturing into a real frontier object or remains too expensive to outrun the already-banked `Sym^3` line

## Follow-on tranche (resumed target cache continuation)

- One more tranche advanced by `3` additional exact windows, to `52 / 65`.
- Bound-resume elapsed approximately `608.87` seconds for this tranche.
- The cached target-side state is now:
  - `state_window_index = 51`
  - `next_window_index = 52`
  - lead state `0`
- The current observed sequence still matches the alternating singularity model: the new cache point remains a rebase-ready state for the next pending step.

## Follow-on tranche (verified continuation to 58 / 65)

At the start of this continuation, the persisted cache was verified directly at
`57 / 65` completed windows:

- `completed_window_count = 57`
- `next_window_index = 57`
- `state_window_index = 56`
- lead state nonzero

A bounded one-window continuation then advanced the cache by one exact target
window:

- progress `58 / 65`
- elapsed approximately `709.99s`
- `next_window_index = 58`
- `state_window_index = 57`
- lead state `0`

This was an ordinary advance from a nonzero lead state. Its elapsed time raises
the observed ordinary-step high-water mark from approximately `606.79s` to
approximately `709.99s`. Because the resulting lead state is now zero, the next
pending quartic target-side step is again predicted to be a rebase case.

## Follow-on tranche (verified continuation to 59 / 65)

The next bounded one-window continuation confirmed that predicted rebase case:

- progress `59 / 65`
- elapsed approximately `1110.89s`
- `next_window_index = 59`
- `state_window_index = 58`
- lead state nonzero

This lifts the observed rebase high-water mark from approximately `813.01s` to
approximately `1110.89s`. Because the resulting lead state is now nonzero, the
next pending quartic target-side step is predicted to be an ordinary advance.

## Follow-on tranche (verified continuation to 60 / 65)

The next bounded one-window continuation confirmed that predicted ordinary
advance:

- progress `60 / 65`
- elapsed approximately `733.21s`
- `next_window_index = 60`
- `state_window_index = 59`
- lead state `0`

This lifts the observed ordinary-step high-water mark from approximately
`709.99s` to approximately `733.21s`. Because the resulting lead state is now
zero, the next pending quartic target-side step is predicted to be a rebase
case.

## Follow-on tranche (verified continuation to 61 / 65)

The next bounded one-window continuation confirmed that predicted rebase case:

- progress `61 / 65`
- elapsed approximately `1225.92s`
- `next_window_index = 61`
- `state_window_index = 60`
- lead state nonzero

This lifts the observed rebase high-water mark from approximately `1110.89s` to
approximately `1225.92s`. Because the resulting lead state is now nonzero, the
next pending quartic target-side step is predicted to be an ordinary advance.
