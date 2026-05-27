"""Vulnerability tier assignment (Low / Medium / High).

Each story view gets its own tier function. Sources are federal or state agencies so
a legend reads as an agency designation, not our opinion. Logic lands per the relevant
Phase 1 subsection; this module fixes the vocabulary and signatures.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd

    from lus_pipeline.config import Config


class Tier(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def assign_flood_tier(parcels: gpd.GeoDataFrame, config: Config) -> gpd.GeoDataFrame:
    """Flood tier from FEMA NFHL + USGS/NOAA models + WA Ecology. Phase 1b."""
    raise NotImplementedError("assign_flood_tier is a Phase 1b task.")


def assign_drought_tier(parcels: gpd.GeoDataFrame, config: Config) -> gpd.GeoDataFrame:
    """Drought tier: composite of USDM frequency, NOAA temp trend, SNOTEL SWE. Phase 1c."""
    raise NotImplementedError("assign_drought_tier is a Phase 1c task.")


def assign_sales_tier(parcels: gpd.GeoDataFrame, config: Config) -> gpd.GeoDataFrame:
    """Land-changing-hands tier from per-parcel and neighborhood sales velocity. Phase 1d."""
    raise NotImplementedError("assign_sales_tier is a Phase 1d task.")


def assign_building_tier(parcels: gpd.GeoDataFrame, config: Config) -> gpd.GeoDataFrame:
    """Building-activity tier from permit density, weighted by permit type. Phase 1e."""
    raise NotImplementedError("assign_building_tier is a Phase 1e task.")
