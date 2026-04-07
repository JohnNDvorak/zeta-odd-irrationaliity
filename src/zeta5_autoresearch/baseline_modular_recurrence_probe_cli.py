from __future__ import annotations

import argparse
from pathlib import Path

from .baseline_modular_recurrence_probe import write_baseline_modular_recurrence_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run modular rank certificates for Brown-Zudilin baseline recurrence degrees.")
    parser.add_argument("--max-n", type=int, default=38, help="Largest baseline index to evaluate modulo each certificate prime.")
    parser.add_argument("--degrees", type=int, nargs="+", default=(8, 9), help="Degrees to test.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_baseline_modular_recurrence_report(
        max_n=args.max_n,
        degrees=tuple(args.degrees),
        output_path=args.output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
