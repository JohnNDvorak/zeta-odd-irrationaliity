# Brown–Zudilin 2026 notes

- Baseline worked example uses `a = (8, 16, 10, 15, 12, 16, 18, 13)`.
- Converted slope vector is `u = (20.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5)`.
- Baseline intercept vector is `v = (0, 0, 0, 0, 0, 0, 0, 0)`.
- In the totally symmetric case `a_1 = ... = a_8 = n`, the paper gives a published third-order recurrence valid for `I_n` and also for `Q_n`, `\hat P_n`, `P_n`.
- Published totally symmetric initial values include `Q_0 = 1`, `Q_1 = 21`, `Q_2 = 2989`.
- Published constants:
  - `C0 = -31.55296934...`
  - `C1 = 85.08768883...`
  - `C2 = 49.60574814...`
  - `gamma = 0.86597135...`
  - `M_proof = -18.05277880...`
- The main strategic hint is that additional arithmetic savings are expected from alternative representations and certificates for the same sequence.
