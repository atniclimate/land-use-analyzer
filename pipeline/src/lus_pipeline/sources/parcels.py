"""Whatcom County GIS parcel shapefile. See DATA_SOURCES.md section 1.

Polygon geometry per tax parcel, keyed by the 16-digit GID (join key to the short
master). Reprojected to the web output CRS on load.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import geopandas as gpd
import httpx

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "parcels"
PHASE = "1a"
_ARCHIVE = "parcels_shapefile.zip"


def fetch(config: Config) -> Path:
    """Stream the parcel shapefile archive to raw_dir. Returns the written path."""
    config.ensure_dirs()
    dest = config.raw_dir / _ARCHIVE
    with (
        httpx.Client(follow_redirects=True, timeout=300.0) as client,
        client.stream("GET", config.sources.parcels_shapefile) as resp,
    ):
        resp.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in resp.iter_bytes(chunk_size=1 << 16):
                fh.write(chunk)
    return dest


def load(config: Config) -> gpd.GeoDataFrame:
    """Read the parcel polygons and reproject to the web output CRS."""
    archive = config.raw_dir / _ARCHIVE
    if not archive.exists():
        raise FileNotFoundError(f"{archive} not found. Run parcels.fetch() first.")
    gdf = gpd.read_file(f"zip://{archive.as_posix()}")
    if gdf.crs is None:
        raise ValueError("Parcel shapefile has no CRS; cannot reproject reliably.")
    return gdf.to_crs(config.web_export.output_crs)
