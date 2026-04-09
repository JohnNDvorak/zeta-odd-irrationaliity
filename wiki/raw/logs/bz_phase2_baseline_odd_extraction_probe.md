# Phase 2 baseline odd extraction probe

- Probe id: `bz_phase2_baseline_odd_extraction_probe_v1`
- Source rule: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_odd_extraction_rule.md`
- Source rule id: `bz_phase2_baseline_odd_extraction_rule_v1`
- Shared exact window: `n=1..80`
- Retained output hash: `9638c96a818b78424eb98e5a3acb7e5a4a74d15c0de5e42b67a6c02ea8e92fa6`
- Unresolved residual hash: `997271ee3fa59dd834d566291294f675d96ca79c60f99e5754986be7043091ab`
- Extraction summary hash: `235cd4bc3db909c8338fd38a9d49319e8d063041f9ec6b00d307c5b2ee148fe6`
- Verdict: `baseline_odd_pair_summary_established`

## Stabilized findings

- A baseline odd-pair extraction summary now exists on the exact shared window `n=1..80`.
- The retained odd-weight output and the unresolved constant residual are independently reproducible via exact hashes.
- The active extraction object is defined directly on baseline-side data and keeps the odd-zeta channels together.

## Unresolved findings

- No baseline `P_n` sequence has been extracted.
- No baseline remainder pipeline has been proved.
- The constant residual remains unresolved rather than eliminated.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration for conventions and failure modes. It may not redefine the active odd-pair object or supply hidden identities for it.

## Sample retained / residual data

| n | retained zeta(5) | retained zeta(3) | unresolved constant |
| --- | --- | --- | --- |
| `1` | `-17062318711073217087874368` | `-3367966716871959076170056761/60` | `57993101249962008127812740936483643927138591089/680932458439833600000` |
| `2` | `152044985550430960231949449314536670627277608934680000` | `208654744620329781862992977733737076830747703633619989058843/417136` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` |
| `3` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` |

## Recommendation

Add the odd-pair post-probe decision gate next. It should decide whether this odd-weight baseline summary is strong enough to justify one bounded residual-refinement ladder.
