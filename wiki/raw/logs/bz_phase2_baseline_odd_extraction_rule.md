# Phase 2 baseline odd extraction rule

- Rule id: `bz_phase2_baseline_odd_extraction_rule_v1`
- Source spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_odd_pair_object_spec.md`
- Source spec id: `bz_phase2_baseline_odd_pair_object_spec`
- Shared exact window: `n=1..80`
- Rule label: Retain `(zeta(5), zeta(3))` as the active odd-weight extraction pair and carry the constant term as unresolved residual
- Retained output hash: `9638c96a818b78424eb98e5a3acb7e5a4a74d15c0de5e42b67a6c02ea8e92fa6`
- Unresolved residual hash: `997271ee3fa59dd834d566291294f675d96ca79c60f99e5754986be7043091ab`
- Extraction summary hash: `235cd4bc3db909c8338fd38a9d49319e8d063041f9ec6b00d307c5b2ee148fe6`

## Rule statement

The bounded odd-pair extraction rule promotes the baseline-side pair `(zeta(5), zeta(3))` to the active extraction output object and carries the rational constant term explicitly as unresolved residual structure. No baseline remainder or bridge-fit identity is asserted.

## Confirmed output

- The retained odd-weight extraction output is an exact repo-native ordered pair over the shared window.
- The unresolved constant residual remains exact and explicit over the same shared window.
- The full odd-pair extraction summary is reproducible via retained and residual hashes.

## Inferred structure

- This rule treats the odd-weight pair as the next baseline-native extraction object after the `(constant, zeta(5))` line hit a hard wall.
- This rule interprets the constant term as residual structure rather than part of the active odd pair.

## Unresolved structure

- No baseline P_n sequence has been extracted.
- No baseline remainder pipeline has been proved.
- No rule eliminating the constant residual is claimed.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration for conventions and failure modes. It may not redefine the active odd-pair object or supply hidden identities for it.

## Sample retained / residual data

| n | retained zeta(5) | retained zeta(3) | unresolved constant |
| --- | --- | --- | --- |
| `1` | `-17062318711073217087874368` | `-3367966716871959076170056761/60` | `57993101249962008127812740936483643927138591089/680932458439833600000` |
| `2` | `152044985550430960231949449314536670627277608934680000` | `208654744620329781862992977733737076830747703633619989058843/417136` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` |
| `3` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` |

## Recommendation

Run one bounded odd-pair extraction probe next and require its report to preserve the split between retained odd channels and unresolved constant residual.
