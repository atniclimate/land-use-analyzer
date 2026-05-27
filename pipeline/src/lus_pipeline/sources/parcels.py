"""Whatcom County GIS parcel shapefile. See DATA_SOURCES.md section 1.

Polygon geometry per tax parcel, keyed by the 16-digit GID (join key to the short
master). Phase 1a. fetch()/load() raise NotImplementedError until implemented.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "parcels"
PHASE = "1a"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
