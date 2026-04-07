from __future__ import annotations

import argparse

from .bz_dual_f7_companion_recurrence_probe import write_bz_dual_f7_companion_recurrence_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the Brown-Zudilin dual F_7 companion recurrence report.")
    parser.add_argument("--output", help="Optional output path for the markdown report.")
    parser.add_argument("--max-n", type=int, default=12, help="Largest exact baseline n-index to include.")
    parser.add_argument("--degree-min", type=int, default=0, help="Smallest polynomial degree to test.")
    parser.add_argument("--degree-max", type=int, default=2, help="Largest polynomial degree to test.")
    args = parser.parse_args()
    output = write_bz_dual_f7_companion_recurrence_report(
        output_path=args.output,
        max_n=args.max_n,
        degree_min=args.degree_min,
        degree_max=args.degree_max,
    )
    print(output)


if __name__ == "__main__":
    main()
