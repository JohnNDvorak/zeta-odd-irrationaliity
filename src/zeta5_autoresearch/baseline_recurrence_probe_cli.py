from __future__ import annotations

import argparse
from pathlib import Path

from .baseline_recurrence_probe import write_baseline_recurrence_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Search for exact polynomial recurrences in the Brown-Zudilin baseline Q_n sequence.")
    parser.add_argument("--max-n", type=int, default=34, help="Largest exact baseline index to compute.")
    parser.add_argument("--degree-min", type=int, default=0, help="Smallest polynomial degree to scan.")
    parser.add_argument("--degree-max", type=int, default=8, help="Largest polynomial degree to scan.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_baseline_recurrence_report(
        max_n=args.max_n,
        degree_min=args.degree_min,
        degree_max=args.degree_max,
        output_path=args.output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
