# Phase 2 dual projection probe

- Probe id: `bz_phase2_dual_projection_probe_v1`
- Target spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_target_spec.md`
- Calibration check: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_calibration_check.md`
- Target id: `baseline_dual_f7_exact_coefficient_packet`
- Calibration anchor id: `zudilin_2002_third_order_zeta5_bridge`
- Shared exact window: `n=1..80`
- Projection-ready packet hash: `8dde8e0e3dca2ced6b0b96eea05422f5afdf497e54e0a812c8b977a7ba9cca6a`

## Calibration matches

- Coefficient-level normalization remains explicit: the probe keeps separate component hashes instead of collapsing to one scalar remainder.
- Companion channels remain explicit: constant, zeta(3), and zeta(5) are all named components in the packet.
- Sequence-level reproducibility is preserved: each component is hashed on an exact shared window and tied to a concrete cache frontier.

## Calibration departures

- The calibration anchor is a published q_n ζ(5) - p_n linear form, whereas this probe only prepares a pre-projection coefficient packet.
- The baseline packet currently has asymmetric component coverage because the zeta(5) exact cache only reaches n=80 while constant and zeta(3) reach n=434.
- No projection rule is asserted yet; this probe only freezes the exact packet that a later projection step may consume.

## Non-claims

- This target is not a published baseline P_n sequence.
- This target is not a proved baseline remainder pipeline.
- This target does not by itself isolate the Brown-Zudilin baseline decay object.

## Components

| component | max verified index | shared window end | provisional hash | first terms |
| --- | --- | --- | --- | --- |
| `constant` | `434` | `80` | `302fe012c87380d69299f7896618d1839fc0cbb48259f591dc8742227ce9fc27` | `57993101249962008127812740936483643927138591089/680932458439833600000, -257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000, 323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` |
| `zeta3` | `434` | `80` | `edcab42214d672a099725841b726480d7d63c8fcc21ba52b31ae95d8642b57c2` | `-3367966716871959076170056761/60, 208654744620329781862992977733737076830747703633619989058843/417136, -21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` |
| `zeta5` | `80` | `80` | `ecb9f95f956fa9fe29d9508be319df61d13920079c6147536ded699f75a14739` | `-17062318711073217087874368, 152044985550430960231949449314536670627277608934680000, -2722389989936502211771784255579458505909144632383999807069362363792300939024160000` |

## Recommendation

Use this shared-window exact packet as the input to the first actual projection rule experiment. Any next probe must report what linear combination or filter is applied to this packet and must keep the departure from the Zudilin 2002 calibration anchor explicit.
