"""Sidecar metadata for the web app.

The parcel features themselves ship as PMTiles (see tiles.py). This module emits a
small JSON next to the tiles describing the tenure source and the parcel count, so
the UI can show "data needed" when tenure is still placeholder.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

import geopandas as gpd

if TYPE_CHECKING:
    from lus_pipeline.config import Config

META_NAME = "parcels.meta.json"


def write_meta(gdf: gpd.GeoDataFrame, config: Config) -> Path:
    """Write parcels.meta.json next to the tiles. Returns the path."""
    config.ensure_dirs()
    tenure_source = str(gdf["tenure_source"].iloc[0]) if len(gdf) else "unknown"
    meta = {
        "tenure_source": tenure_source,
        "parcel_count": int(len(gdf)),
        "generated": date.today().isoformat(),
    }
    dest = config.tiles_output_dir / META_NAME
    dest.write_text(json.dumps(meta, indent=2))
    return dest
