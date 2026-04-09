# Phase 2 external calibration check

- Check id: `bz_phase2_external_calibration_check`
- Chosen anchor id: `zudilin_2002_third_order_zeta5_bridge`
- Chosen source: `Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)`
- Chosen location: `Theorem 1, equations (1) and (2)`
- Literature verification report: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_literature_verification_report.md`
- Dual projection plan: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_experiment_plan.md`
- Dual projection target spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_target_spec.md`

## Why this anchor

This is the strongest checked external bridge object because it publishes an explicit zeta(5) linear form q_n ζ(5) - p_n together with a companion zeta(3) channel. That makes it the closest verified analog to the baseline dual coefficient packet without pretending that the Brown-Zudilin baseline seed itself is explicit.

## Rejected alternatives

- Zudilin 2002 odd-zeta paper: explicit but more generic; weaker as a convention lock than a single stated recurrence object.
- Zudilin 2018 hypergeometric-integrals note: explicit building blocks, but less direct as a first calibration target than q_n ζ(5) - p_n.
- McCarthy-Osburn-Straub 2020: denominator-side cellular data only; not a decay-side coefficient anchor.

## Calibration invariants

### linear_form_normalization

- Statement: The calibration anchor must be treated as an explicit linear form with a separated zeta(5) coefficient and rational term, not as a black-box numeric remainder.
- Why it matters: The first baseline projection probe should preserve coefficient-level bookkeeping and must not collapse its target into an opaque scalar too early.

### parasitic_channel_explicitness

- Statement: A companion non-zeta(5) channel, here the zeta(3) side, should remain explicit instead of being hidden inside a single projected object.
- Why it matters: The baseline dual target also carries companion channels, so the probe needs conventions that record those channels honestly before any projection claim.

### sequence_level_reproducibility

- Statement: The calibration anchor must be tied to published sequence-level data or recurrence data that another implementer could reproduce.
- Why it matters: The baseline projection program should only promote objects whose conventions can be checked against an explicit reference, not just against our own internal extraction choices.

## Success condition

The next baseline projection probe adopts these three invariants explicitly and names where its target object matches or departs from the external calibration anchor.

## Next probe contract

The first bounded baseline projection probe must consume the baseline dual F_7 exact coefficient packet, state its coefficient-level normalization explicitly, preserve companion channels as named components, and report any asymmetry in component coverage before making a projection claim.
