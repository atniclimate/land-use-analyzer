"""Ownership classification.

Implements the tenure-gated hierarchy in CLAUDE.md. The classification logic lands
in Phase 1a; this module fixes the vocabulary (categories, public signatures) so the
rest of the pipeline can be wired against it.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd

    from lus_pipeline.config import Config


class OwnershipCategory(StrEnum):
    """First-match-wins hierarchy. Order matters: the first matching rule wins."""

    GOVERNMENT_TRIBAL_UTILITY = "government_tribal_utility"
    CONCENTRATED_CORPORATE = "concentrated_corporate"
    SMALL_CORPORATE = "small_corporate"
    OUT_OF_STATE = "out_of_state"
    FOREIGN = "foreign"
    LOCAL = "local"


# Categories gated by the per-parcel tenure rule. A parcel lands in one of these
# only when the current owner's tenure is under Thresholds.tenure_years (default 30).
# Established owners (30+ years) stay neutral regardless of mailing address.
TENURE_GATED: tuple[OwnershipCategory, ...] = (
    OwnershipCategory.CONCENTRATED_CORPORATE,
    OwnershipCategory.OUT_OF_STATE,
    OwnershipCategory.FOREIGN,
)


def classify_parcels(parcels: gpd.GeoDataFrame, config: Config) -> gpd.GeoDataFrame:
    """Return parcels with `ownership_category` and `tenure_years` columns.

    Phase 1a. See PHASE_PLAN.md section 1a and CLAUDE.md, "Classification thresholds".
    """
    raise NotImplementedError("classify_parcels is a Phase 1a task. See PHASE_PLAN.md.")
