# Phase 2 dual projection rule experiment

- Experiment id: `bz_phase2_dual_projection_rule_experiment_v1`
- Rule id: `keep_constant_and_zeta5_carry_zeta3_residual_v1`
- Rule label: Keep `(constant, zeta(5))` as the retained pair and carry `zeta(3)` as an explicit residual channel
- Source packet report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_probe.md`
- Calibration report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_external_calibration_check.md`
- Shared exact window: `n=1..80`
- Source packet hash: `8dde8e0e3dca2ced6b0b96eea05422f5afdf497e54e0a812c8b977a7ba9cca6a`
- Retained pair hash: `c09c3939d1f2eda843de8f8a9191ab71ba9e14770a33cc0d9150b1b591e8cbc0`
- Residual channel hash: `a77ea420009d5ce76ed63e7c75bf1f63ad6832813958f196c8b8b81d870ea3c3`

## Rule meaning

This is a bookkeeping projection rule inspired by the odd-target isolation idea in the verified literature. It does not set the zeta(3) channel to zero or claim a motivic projection theorem. It only freezes the two-channel `(constant, zeta(5))` pair as the retained target while carrying the exact zeta(3) channel as an explicit residual companion on the same shared window.

## Matches to calibration

- The retained object is still a coefficient-level linear-form object rather than a black-box scalar.
- The companion zeta(3) channel remains explicit as residual data instead of being hidden.
- The retained pair and residual channel are both hashed on the same exact shared window, preserving reproducibility.

## Departures from calibration

- The calibration anchor gives a published q_n ζ(5) - p_n linear form, while this rule only defines a retained pair and residual channel.
- The rule is bookkeeping-only: it does not derive a recurrence or prove that the residual channel can be eliminated.
- The retained pair still inherits the baseline packet's shorter shared window n<=80 because the zeta(5) cache is the limiting component.

## Non-claims

- This rule does not prove that the retained pair equals a baseline P_n or baseline remainder sequence.
- This rule does not justify dropping the zeta(3) channel analytically; it only records it separately as residual data.
- This rule does not claim any irrationality consequence by itself.

## Sample retained / residual data

| n | retained constant | retained zeta(5) | residual zeta(3) |
| --- | --- | --- | --- |
| `1` | `57993101249962008127812740936483643927138591089/680932458439833600000` | `-17062318711073217087874368` | `-3367966716871959076170056761/60` |
| `2` | `-257175662867915336128611999275663352912980024753994727140390860579349038684288337681979334351609/338862506490277085099028692131356672000000` | `152044985550430960231949449314536670627277608934680000` | `208654744620329781862992977733737076830747703633619989058843/417136` |
| `3` | `323525731241233942713669947799685961885190714855105471401501251353465286528857031397850200738249602831976998887933914370005906391564677541343706400257/23808072749798504607737701394874902256375179017482026355483648000000` | `-2722389989936502211771784255579458505909144632383999807069362363792300939024160000` | `-21267080533261503179629889087083778589656840684201594171947828180831792407606895913942705929/2374537572` |

## Recommendation

Use this retained-pair / residual-channel split as the baseline for the next decision gate. The next step should either propose one stronger projection identity to test against this split or stop and fall back to the external bridge path.
