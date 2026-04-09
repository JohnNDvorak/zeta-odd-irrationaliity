# Phase 2 symmetric-to-baseline transfer probe

- Probe id: `bz_phase2_symmetric_baseline_transfer_probe`
- Source spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_baseline_transfer_object_spec.md`
- Source spec id: `bz_phase2_symmetric_baseline_transfer_object_spec`
- Shared exact window: `n=1..80`
- Source packet hash: `29e49aff6501454dee8869ac44e2b82abf96fb56b51185b3f5747fa211c5e316`
- Target packet hash: `b062473999b0fc82c3975d5e2bcfec8ddbc69eff8c8c2edbb67c374d8f0baf1b`
- Transfer object hash: `d86d2f79156574b679780b6eddb215d1914ef396b59712239f7569c3f4d669ed`
- Verdict: `symmetric_baseline_transfer_object_established`

## Stabilized findings

- A paired source/target exact transfer object now exists on the shared window `n=1..80`.
- The source side is recurrence-explicit and source-backed; the target side is the exact baseline dual full packet.
- Both packets and the paired transfer object are independently reproducible via exact hashes.

## Unresolved findings

- No transfer map has been certified.
- No baseline recurrence has been imported from the source family.
- No baseline P_n or baseline remainder pipeline has been extracted from the transfer object.

## Source boundary

A transfer success would still be a packet-level relation on a finite exact window. It would not by itself prove baseline equivalence, baseline P_n extraction, or a baseline remainder pipeline.

## Sample paired packet data

| n | source scaled Q | source scaled P | source scaled Phat | target constant | target zeta(3) | target zeta(5) |
| --- | --- | --- | --- | --- | --- | --- |
| `1` | `21` | `87/4` | `101/2` | `57993101249962008127812740936483643927138591089/680932458439833600000` | `-3367966716871959076170056761/60` | `-17062318711073217087874368` |
| `2` | `95648` | `1190161/12` | `344923/2` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` | `208654744620329781862992977733737076830747703633619989058843/417136` | `152044985550430960231949449314536670627277608934680000` |
| `3` | `5556333024` | `23046063717/4` | `3710571371/2` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` |

## Recommendation

Run one bounded packet-level transfer family ladder next: constant map, difference map, and lag-1 map.
