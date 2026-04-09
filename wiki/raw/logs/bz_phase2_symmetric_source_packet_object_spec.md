# Phase 2 symmetric source packet object spec

- Spec id: `bz_phase2_symmetric_source_packet_object_spec`
- Prior hard-wall gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_full_packet_compression_decision_gate.md`
- Source packet id: `bz_totally_symmetric_scaled_linear_forms_packet`
- Source family: `totally_symmetric_linear_form_pipeline`
- Object label: `Totally symmetric scaled coefficient packet`
- Object kind: `source_backed_scaled_exact_coefficient_packet`

## Object semantics

The active family-source object is the scaled totally symmetric coefficient triple `(d_n^5 Q_n, d_n^5 P_n, d_n^2 d_{2n} P̂_n)` on the shared exact window `n=1..80`. This keeps the published arithmetic scales explicit and treats the totally symmetric linear-form pipeline as a recurrence-explicit source family rather than as a baseline surrogate.

## Rationale

The baseline dual packet has now exhausted low-complexity pairwise compression in all three orientations. The next honest source pivot is the repo's source-backed totally symmetric remainder / linear-form pipeline, because it is genuinely sequence-explicit and structurally different from the exhausted baseline packet.

## Components

| component | role | scale | max verified index | exact status |
| --- | --- | --- | --- | --- |
| `scaled_q` | scaled zeta(5) leading coefficient channel | `d_n^5` | `80` | `exact` |
| `scaled_p` | scaled rational zeta(5) companion coefficient channel | `d_n^5` | `80` | `exact` |
| `scaled_phat` | scaled zeta(2)-side companion coefficient channel | `d_n^2 d_2n` | `80` | `exact` |

## Component notes

- `scaled_q`: This is the scaled source-backed denominator-side channel from the published totally symmetric recurrence.
- `scaled_p`: This is the scaled source-backed rational coefficient paired with the linear form `Q_n zeta(5) - P_n`.
- `scaled_phat`: This remains explicit to keep the totally symmetric linear-form decomposition honest at the coefficient level.

## Source boundary

This source-backed packet is not the Brown-Zudilin baseline seed. It may guide family-source experiments and calibration, but it may not be silently transferred into a claimed baseline `P_n` or baseline remainder object.

## Non-claims

- This spec does not claim equivalence between the totally symmetric source family and the Brown-Zudilin baseline seed.
- This spec does not claim a baseline extraction.
- This spec does not privilege one pairwise compression route before exact testing inside the symmetric source family.

## Recommended next step

Hash and probe the scaled symmetric source packet first, then run one bounded pairwise compression layer across all three residual orientations.
