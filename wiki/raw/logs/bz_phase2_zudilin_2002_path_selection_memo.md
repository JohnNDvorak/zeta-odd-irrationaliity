# Phase 2 Zudilin 2002 path-selection memo

- Memo id: `bz_phase2_zudilin_2002_path_selection_memo`
- Shared exact window: `n=1..7`
- Coupled-map decision gate: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_zudilin_2002_coupled_map_decision_gate.md`
- Construction memo: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_construction_memo.md`

## Premise

The bounded constant-form ansatz layer is closed on the shared window. The next move should maximize research signal rather than continue ansatz inflation by momentum.

## Options

| option | recommendation | objective | upside | downside |
| --- | --- | --- | --- | --- |
| `n_dependent_coupled_map` | `secondary` | Test one bounded two-channel family with explicit n-dependence, such as an affine-in-n 2x2 matrix, against the ordered pair `(ζ(5), ζ(3))`. | Natural next escalation from the constant coupled map and still close to the current bridge-comparison machinery. | High risk of turning into another mechanical ansatz climb without improving proof relevance. |
| `different_paired_object` | `secondary` | Change the compared paired object itself instead of changing only the map family, for example by altering the baseline-side retained/residual packaging or the bridge-side target object. | Could reveal that the current pair is simply the wrong abstraction, avoiding uninformative map-fitting. | Requires a fresh design choice and may partially reset comparison continuity. |
| `baseline_extraction_path` | `primary` | Use the bridge work as calibration only, and shift back toward building a baseline-family extraction step that is more proof-relevant than further bridge-map fitting. | Best alignment with the long-term goal: explicit baseline decay-side structure rather than more indirect analogies. | Harder engineering and math, with a less immediate bounded experiment than the map-fitting line. |

## Chosen path

- `baseline_extraction_path`

## Rationale

The bridge program has now done what it needed to do: it produced a disciplined comparison object and closed several low-complexity map families. That is enough calibration. The next best use of cycles is to redirect toward baseline-side extraction or projection construction, not to keep expanding the bridge ansatz catalog.

## Stop rules

- Do not add cubic or higher one-channel normalization maps unless a new structural reason appears.
- Do not add arbitrary n-dependent 2x2 map families without first stating a bounded motivating principle.
- If a new bridge-side experiment is proposed, it must explain why it advances baseline extraction rather than only enlarging the ansatz catalog.
