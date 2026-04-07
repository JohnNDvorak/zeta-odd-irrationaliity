from __future__ import annotations

import argparse
from pathlib import Path

from .bz_symmetric_linear_forms_probe import write_bz_totally_symmetric_linear_forms_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Brown-Zudilin totally symmetric linear-form probe.")
    parser.add_argument("--max-n", type=int, default=12, help="Largest totally symmetric index to generate exactly.")
    parser.add_argument("--precision", type=int, default=80, help="Decimal precision for numeric remainder estimates.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_bz_totally_symmetric_linear_forms_report(
        max_n=args.max_n,
        precision=args.precision,
        output_path=args.output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
