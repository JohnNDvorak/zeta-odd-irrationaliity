# Phase 2 baseline full-packet probe

- Probe id: `bz_phase2_baseline_full_packet_probe`
- Source spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_full_packet_object_spec.md`
- Source spec id: `bz_phase2_baseline_full_packet_object_spec`
- Shared exact window: `n=1..80`
- Packet hash: `f2abd1cabc79e64b46a56a850a2ad2f0f1b661170e9c84153395b9fb1bfe31e5`
- Verdict: `baseline_full_packet_established`

## Stabilized findings

- A baseline-native full coefficient packet now exists on the exact shared window `n=1..80`.
- The packet hash is reproducible and does not privilege any pairwise compression route a priori.
- All three exact channels are held active simultaneously at object-definition time.

## Unresolved findings

- No baseline `P_n` sequence has been extracted.
- No baseline remainder pipeline has been proved.
- No pairwise compression route has yet been selected or certified.

## Bridge boundary

The Zudilin 2002 bridge stack remains calibration-only. It may not redefine the packet or choose a preferred compression route.

## Sample packet data

| n | constant | zeta(3) | zeta(5) |
| --- | --- | --- | --- |
| `1` | `57993101249962008127812740936483643927138591089/680932458439833600000` | `-3367966716871959076170056761/60` | `-17062318711073217087874368` |
| `2` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` | `208654744620329781862992977733737076830747703633619989058843/417136` | `152044985550430960231949449314536670627277608934680000` |
| `3` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` |

## Recommendation

Run the bounded full-packet compression layer next, using the two prior hard-wall gates plus one new zeta(5)-residual route.
