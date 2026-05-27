# Land Use Analyzer pipeline

Python data pipeline. Fetches public agency data, classifies parcels by ownership,
assigns vulnerability tiers, and builds PMTiles for the web app.

This is the Phase 0 skeleton. The CLI, configuration, and source registry are real.
The fetch, classify, tier, and tile steps raise `NotImplementedError` until their
Phase 1 subsection lands (see `PHASE_PLAN.md`).

## Prerequisites

- Python 3.11 or newer.
- [uv](https://docs.astral.sh/uv/) for dependency management.
- For tile generation (Phase 1a and later), two external binaries on your `PATH`:
  - [tippecanoe](https://github.com/felt/tippecanoe)
  - [pmtiles CLI](https://github.com/protomaps/go-pmtiles)

## Setup

```powershell
# PowerShell - for the user to run
cd C:\dev\land-use-analyzer\pipeline
uv sync
```

## Common commands

```powershell
# PowerShell - for the user to run
uv run lus-refresh --help
uv run lus-refresh --list-sources
uv run lus-refresh --dry-run
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Layout

```
src/lus_pipeline/
  config.py          paths and editorial thresholds (tenure, concentration)
  classify.py        ownership classification (tenure-gated hierarchy)
  tier.py            vulnerability tier assignment (Low / Medium / High)
  tiles.py           tippecanoe + PMTiles wrapper
  refresh.py         orchestrator and CLI entry point (lus-refresh)
  sources/           one module per data source; each exposes fetch() and load()
    permits/         one module per jurisdiction
tests/               smoke tests now; fixture-based classification tests in Phase 1a
scripts/refresh.sh   convenience wrapper: uv sync then lus-refresh
```

Outputs land in `../webapp/public/tiles/`. See `../DATA_SOURCES.md` for every source
and `../ARCHITECTURE.md` for the overall shape.
