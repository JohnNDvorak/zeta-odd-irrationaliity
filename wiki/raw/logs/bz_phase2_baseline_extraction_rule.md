# Phase 2 baseline extraction rule

- Rule id: `bz_phase2_baseline_extraction_rule_v1`
- Source spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_pair_object_spec.md`
- Source spec id: `bz_phase2_baseline_pair_object_spec`
- Shared exact window: `n=1..80`
- Rule label: Retain `(constant, zeta(5))` as extraction output and carry `zeta(3)` as unresolved residual
- Retained output hash: `5ef55ab786310fff419ba0251642a1952db2692a81307ae447bc2c05bb326113`
- Unresolved residual hash: `0dafbe0d0f73c5ea5c3bb7589e52d3720ceda29f29b7603a8caed8e5e09fc585`
- Extraction summary hash: `575370f4687786a411255200eab9ab1f72ad8c44fed8e0563f9914496a6d8f56`

## Rule statement

The bounded extraction rule promotes the baseline-side pair `(constant, zeta(5))` to the active extraction output object and carries the `zeta(3)` channel explicitly as unresolved residual structure. No elimination or bridge-fit identity is asserted.

## Confirmed output

- The retained extraction output is an exact repo-native ordered pair over the shared window.
- The unresolved residual `zeta(3)` channel remains exact and explicit over the same shared window.
- The full extraction summary is reproducible via retained and residual hashes.

## Inferred structure

- This rule treats the retained pair as the first bounded baseline extraction output type.
- This rule interprets the `zeta(3)` channel as unresolved structure rather than disposable noise.

## Unresolved structure

- No baseline P_n sequence has been extracted.
- No baseline remainder pipeline has been proved.
- No rule eliminating the residual `zeta(3)` channel is claimed.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration to sanity-check bookkeeping conventions and failure modes. It may not redefine the active baseline object or supply hidden identities for it.

## Sample retained / residual data

| n | retained constant | retained zeta(5) | unresolved zeta(3) |
| --- | --- | --- | --- |
| `1` | `57993101249962008127812740936483643927138591089/680932458439833600000` | `-17062318711073217087874368` | `-3367966716871959076170056761/60` |
| `2` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` | `152044985550430960231949449314536670627277608934680000` | `208654744620329781862992977733737076830747703633619989058843/417136` |
| `3` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` |

## Recommendation

Run one bounded extraction probe next and require its report to preserve the split between confirmed retained output and unresolved residual structure.
