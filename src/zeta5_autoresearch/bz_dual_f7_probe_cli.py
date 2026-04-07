from __future__ import annotations

import argparse
from pathlib import Path

from .bz_dual_f7_probe import write_bz_dual_f7_probe_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Brown-Zudilin dual F_7 probe.")
    parser.add_argument("--precision", type=int, default=120, help="Decimal precision for F_7 evaluation.")
    parser.add_argument("--pslq-precision", type=int, default=180, help="Decimal precision for PSLQ search.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_bz_dual_f7_probe_report(
        precision=args.precision,
        pslq_precision=args.pslq_precision,
        output_path=args.output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
