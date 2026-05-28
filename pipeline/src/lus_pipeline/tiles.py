"""Vector tile generation: PMTiles via pyogrio's bundled GDAL.

pyogrio 0.10+ exposes the GDAL 3.8 PMTiles vector writer, which handles MVT
encoding and Hilbert ordering in one step. No tippecanoe / WSL / Docker needed on
Windows. The downstream archive is read by the web app via the pmtiles JS lib and
deck.gl's tile layer.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pyogrio

if TYPE_CHECKING:
    import geopandas as gpd

    from lus_pipeline.config import Config

OUTPUT_NAME = "parcels.pmtiles"
LAYER_NAME = "parcels"

# Columns kept in the per-feature properties. tenure_source is constant per build
# and goes in the meta sidecar instead.
_DROP_COLUMNS = ("tenure_source", "geo_id", "mailing_city")


def build_parcel_pmtiles(gdf: gpd.GeoDataFrame, config: Config) -> Path:
    """Write the classified parcels to a single-layer PMTiles archive. Returns the path.

    Min/max zoom target cadastral use: county overview at z10, parcel-level at z14.
    """
    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
        raise ValueError(f"Parcels must be EPSG:4326 before tiling, got {gdf.crs}")

    config.ensure_dirs()
    dest = config.tiles_output_dir / OUTPUT_NAME
    if dest.exists():
        dest.unlink()

    keep = [c for c in gdf.columns if c not in _DROP_COLUMNS]
    pyogrio.write_dataframe(
        gdf[keep],
        dest,
        driver="PMTiles",
        layer=LAYER_NAME,
        dataset_options={
            "MINZOOM": "8",
            "MAXZOOM": "14",
        },
    )
    return dest
