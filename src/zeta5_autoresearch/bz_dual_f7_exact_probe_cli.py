from __future__ import annotations

import argparse
from pathlib import Path

from .bz_dual_f7_exact_probe import write_bz_dual_f7_exact_probe_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Brown-Zudilin dual F_7 exact probe.")
    parser.add_argument("--precision", type=int, default=120, help="Decimal precision for numeric verification.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_bz_dual_f7_exact_probe_report(precision=args.precision, output_path=args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
