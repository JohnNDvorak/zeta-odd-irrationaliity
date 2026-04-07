from __future__ import annotations

import argparse
from pathlib import Path

from .bz_symmetric_recurrence_probe import write_bz_totally_symmetric_recurrence_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Brown-Zudilin totally symmetric recurrence anchor report.")
    parser.add_argument("--max-n", type=int, default=10, help="Largest n to compare exactly.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_bz_totally_symmetric_recurrence_report(max_n=args.max_n, output_path=args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
