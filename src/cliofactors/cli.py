"""Offline CLI for dataset discovery, inspection and reproducible analysis."""

import argparse
from pathlib import Path
import sys

from . import __version__
from .catalog import all_datasets, dataset
from .data import list_series, load_series, verify_checksums
from .reporting import REFERENCE_SELECTION, Selection, run_analysis


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cliofactors", description="Offline-first historical economics research toolkit",
    )
    parser.add_argument("--version", action="version", version=f"ClioFactors {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("catalog", help="List the seven bundled historical data snapshots")

    series = commands.add_parser("series", help="List series identifiers and annual coverage")
    series.add_argument("dataset", help="Dataset slug shown in catalog")
    series.add_argument("--contains", default="", help="Substring match in series ID or description")
    series.add_argument("--limit", type=int, default=30, help="Maximum listed series (0 for all)")

    inspect = commands.add_parser("inspect", help="Print historical observations for one series")
    inspect.add_argument("dataset")
    inspect.add_argument("series_id")
    inspect.add_argument("--limit", type=int, default=12)

    verify = commands.add_parser("verify", help="Check bundled dataset SHA-256 checksums")

    reproduce = commands.add_parser("reproduce", help="Reproduce Douglas Massachusetts manufacturing analysis")
    reproduce.add_argument("--out", type=Path, default=Path("results/massachusetts-manufacturing"))
    reproduce.add_argument("--no-plots", action="store_true")
    reproduce.add_argument("--hac-lags", type=int, default=2)

    fit = commands.add_parser("fit", help="Fit any three series from one bundled dataset")
    fit.add_argument("--dataset", required=True)
    fit.add_argument("--output-id", required=True)
    fit.add_argument("--capital-id", required=True)
    fit.add_argument("--labor-id", required=True)
    fit.add_argument("--start-year", type=int)
    fit.add_argument("--end-year", type=int)
    fit.add_argument("--spec", choices=["levels", "growth", "both"], default="both")
    fit.add_argument("--hac-lags", type=int, default=2)
    fit.add_argument("--out", type=Path, default=Path("results/custom-fit"))
    fit.add_argument("--no-plots", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "catalog":
            for item in all_datasets():
                print(f"{item.slug:20} {item.title}")
            return 0
        if args.command == "series":
            dataset(args.dataset)
            if args.limit < 0:
                raise ValueError("--limit must be >= 0")
            table = list_series(args.dataset, contains=args.contains)
            if table.empty:
                print("No matching series")
                return 0
            if args.limit:
                table = table.head(args.limit)
            print(table.to_string(index=False, max_colwidth=80))
            return 0
        if args.command == "inspect":
            if args.limit < 0:
                raise ValueError("--limit must be >= 0")
            values = load_series(args.dataset, args.series_id)
            print(f"{args.dataset}/{args.series_id}: {len(values)} annual values")
            print((values.head(args.limit) if args.limit else values).to_string())
            return 0
        if args.command == "verify":
            checks = verify_checksums()
            for name, ok in checks.items():
                print(f"{'OK' if ok else 'MISMATCH'} {name}")
            return 0 if checks and all(checks.values()) else 1
        if args.command in {"reproduce", "fit"}:
            if args.command == "reproduce":
                selected = REFERENCE_SELECTION
                specs = ("levels", "growth")
            else:
                selected = Selection(
                    slug=args.dataset,
                    output_id=args.output_id,
                    capital_id=args.capital_id,
                    labor_id=args.labor_id,
                    start_year=args.start_year,
                    end_year=args.end_year,
                )
                specs = ("levels", "growth") if args.spec == "both" else (args.spec,)
            manifest = run_analysis(
                selected, args.out, specifications=specs,
                hac_lags=args.hac_lags, plots=not args.no_plots,
            )
            print(f"Wrote {', '.join(manifest['specifications'])} analysis to {args.out.resolve()}")
            print(f"Source SHA-256: {manifest['source_sha256']}")
            return 0
        return 2
    except (ValueError, FileNotFoundError, OSError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
