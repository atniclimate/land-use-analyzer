#!/usr/bin/env bash
# Refresh all data sources and rebuild tiles. Run from the pipeline/ directory.
# See DATA_SOURCES.md for the per-source refresh cadence.
#
# Prerequisites (installed separately, not Python packages):
#   - tippecanoe: https://github.com/felt/tippecanoe
#   - pmtiles CLI: https://github.com/protomaps/go-pmtiles
set -euo pipefail

cd "$(dirname "$0")/.."

uv sync
uv run lus-refresh "$@"
