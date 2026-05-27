"""USGS Flood Inundation Mapper. See DATA_SOURCES.md section 2.

Modeled inundation extents at various stream stages, gauged to specific
streamgages. Not all Whatcom streams are gauged; the Nooksack is covered. Phase 1b.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "usgs_inundation"
PHASE = "1b"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
