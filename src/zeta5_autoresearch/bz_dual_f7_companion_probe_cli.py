from __future__ import annotations

import argparse

from .bz_dual_f7_companion_probe import write_bz_dual_f7_companion_probe_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the Brown-Zudilin dual F_7 companion exact-coefficient report.")
    parser.add_argument("--output", help="Optional output path for the markdown report.")
    parser.add_argument("--baseline-term-count", type=int, default=6, help="Number of baseline terms to include.")
    parser.add_argument("--symmetric-term-count", type=int, default=4, help="Number of symmetric-anchor terms to include.")
    args = parser.parse_args()
    output = write_bz_dual_f7_companion_probe_report(
        output_path=args.output,
        baseline_term_count=args.baseline_term_count,
        symmetric_term_count=args.symmetric_term_count,
    )
    print(output)


if __name__ == "__main__":
    main()
