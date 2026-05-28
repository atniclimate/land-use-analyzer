"""Pipeline orchestrator: fetch -> classify -> tier -> tile.

Phase 0 status: this is a runnable skeleton. The source modules, classification,
tiering, and tile steps raise NotImplementedError until their Phase 1 subsection
lands (see PHASE_PLAN.md). The CLI, argument parsing, and source registry are real,
so the rest of the project can be wired against them.

Usage:
    lus-refresh --help
    lus-refresh --list-sources
    lus-refresh --dry-run
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator
from typing import TYPE_CHECKING

from lus_pipeline.config import load_config
from lus_pipeline.sources import SOURCE_GROUPS

if TYPE_CHECKING:
    from lus_pipeline.config import Config


def _iter_sources() -> Iterator[tuple[str, str]]:
    for group, names in SOURCE_GROUPS.items():
        for name in names:
            yield group, name


def list_sources() -> None:
    print("Registered data sources (grouped). See DATA_SOURCES.md for details.\n")
    for group, names in SOURCE_GROUPS.items():
        print(f"  {group}:")
        for name in names:
            print(f"    - {name}")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lus-refresh",
        description=(
            "Land Use Analyzer data pipeline: fetch public agency data, classify "
            "parcels by ownership, assign vulnerability tiers, and build PMTiles."
        ),
    )
    parser.add_argument(
        "--list-sources", action="store_true", help="List registered data sources and exit."
    )
    parser.add_argument("--only", nargs="+", metavar="SOURCE", help="Run only these named sources.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the plan without fetching or building."
    )
    return parser


def build_parcels(config: Config) -> int:
    """Fetch parcels + short master, classify, and write PMTiles + meta. Phase 1a."""
    from lus_pipeline import classify, export, tiles
    from lus_pipeline.sources import parcels, short_master

    print("Fetching short master...")
    short_master.fetch(config)
    print("Fetching parcels...")
    parcels.fetch(config)

    print("Loading and classifying...")
    sm = short_master.load(config)
    gdf = parcels.load(config)
    classified = classify.classify_parcels(gdf, sm, config)

    counts = classified["ownership_category"].value_counts().to_dict()
    source = classified["tenure_source"].iloc[0] if len(classified) else "n/a"
    print(f"Classified {len(classified)} parcels. Tenure source: {source}")
    for category, count in counts.items():
        print(f"  {category}: {count}")

    pmtiles_path = tiles.build_parcel_pmtiles(classified, config)
    meta_path = export.write_meta(classified, config)
    size_mb = pmtiles_path.stat().st_size / 1e6
    print(f"Wrote {pmtiles_path} ({size_mb:.1f} MB)")
    print(f"Wrote {meta_path}")
    if source == "placeholder":
        print("NOTE: tenure is PLACEHOLDER demo data; recency flags are not real yet.")
    return 0


def run(config: Config, only: list[str] | None, dry_run: bool) -> int:
    selected = [(g, n) for g, n in _iter_sources() if only is None or n in only]
    if not selected:
        print("No matching sources.", file=sys.stderr)
        return 1

    print("Land Use Analyzer pipeline.")
    print(f"Data dir:  {config.data_dir}")
    print(f"Web data:  {config.web_data_dir}")
    print("\nPlanned order: fetch -> classify -> tier -> tile\n")
    print("Sources:")
    for group, name in selected:
        print(f"  [{group}] {name}")

    if dry_run:
        print("\nDry run: nothing fetched or built.")
        return 0

    selected_groups = {group for group, _ in selected}
    if "parcels" in selected_groups:
        print("\n=== parcels ===")
        build_parcels(config)

    other = selected_groups - {"parcels"}
    if other:
        print(f"\nNot implemented yet (see PHASE_PLAN.md): {', '.join(sorted(other))}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.list_sources:
        list_sources()
        return 0
    config = load_config()
    return run(config, only=args.only, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
