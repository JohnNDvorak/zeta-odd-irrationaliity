from __future__ import annotations

import argparse
from pathlib import Path

from .bz_dual_f7_zeta5_modular_recurrence_probe import write_bz_dual_f7_zeta5_modular_recurrence_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Brown-Zudilin dual F_7 zeta(5)-coefficient modular recurrence probe.")
    parser.add_argument("--max-n", type=int, default=30, help="Largest n to generate exactly.")
    parser.add_argument("--degrees", type=int, nargs="+", default=[0, 1, 2, 3, 4, 5, 6], help="Degrees to scan.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_bz_dual_f7_zeta5_modular_recurrence_report(
        max_n=args.max_n,
        degrees=tuple(args.degrees),
        output_path=args.output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
