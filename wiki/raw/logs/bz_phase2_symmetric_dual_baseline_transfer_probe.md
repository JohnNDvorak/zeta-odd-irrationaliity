# Phase 2 symmetric-dual to baseline-dual transfer probe

- Probe id: `bz_phase2_symmetric_dual_baseline_transfer_probe`
- Source spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_dual_baseline_transfer_object_spec.md`
- Source spec id: `bz_phase2_symmetric_dual_baseline_transfer_object_spec`
- Shared exact window: `n=1..80`
- Source packet hash: `b14b17274100b7399d1a632bed4ba5a5945be949e76902b8b576f9440d1ef9e5`
- Target packet hash: `6932f65d27763bef2e7b16098d9683acd47cae0589bd72584270188f33e5eecc`
- Transfer object hash: `43f3e1d214b51c0fb1b7a0d068cfda6fbf004b7697e345932c6dc8ae4a459a50`
- Verdict: `symmetric_dual_baseline_transfer_object_established`

## Stabilized findings

- A paired exact dual-packet transfer object now exists on the shared window `n=1..80`.
- Source and target packets now share the same coefficient basis `(constant, zeta(3), zeta(5))` and the same exact extraction family.
- Source, target, and paired transfer objects are independently reproducible via exact hashes.

## Unresolved findings

- No transfer map has been certified.
- No symmetric dual packet identity has been imported into the baseline dual packet.
- No baseline P_n or baseline remainder pipeline has been extracted from this transfer object.

## Source boundary

A transfer success would still be a bounded packet-level relation on `n=1..80`. It would not by itself prove baseline equivalence, a baseline recurrence, or a baseline remainder pipeline.

## Sample paired packet data

| n | source constant | source zeta(3) | source zeta(5) | target constant | target zeta(3) | target zeta(5) |
| --- | --- | --- | --- | --- | --- | --- |
| `1` | `-98` | `66` | `18` | `57993101249962008127812740936483643927138591089/680932458439833600000` | `-3367966716871959076170056761/60` | `-17062318711073217087874368` |
| `2` | `-74463/16` | `6125/2` | `938` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` | `208654744620329781862992977733737076830747703633619989058843/417136` | `152044985550430960231949449314536670627277608934680000` |
| `3` | `-1498833983/3888` | `1524635/6` | `77202` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` |

## Recommendation

Run one bounded low-complexity packet-map ladder next: constant, difference, and lag-1 maps.
