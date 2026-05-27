"""Vector tile generation: tippecanoe + PMTiles conversion.

Wraps the external `tippecanoe` and `pmtiles` binaries (installed separately, not
Python packages). Logic lands in Phase 1a alongside the first parcel tiles.

Prerequisites (not pip-installable):
- tippecanoe: https://github.com/felt/tippecanoe
- pmtiles CLI: https://github.com/protomaps/go-pmtiles
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

TIPPECANOE_BIN = "tippecanoe"
PMTILES_BIN = "pmtiles"


def build_story_tiles(view: str, config: Config) -> Path:
    """Build a PMTiles file for one story view into config.tiles_output_dir. Phase 1a.

    One file per story view, with only the layers that view needs. The parcel base
    layer is shared; story-specific styling is computed client-side.
    """
    raise NotImplementedError(
        "build_story_tiles is a Phase 1a task. Requires tippecanoe and pmtiles on PATH."
    )
