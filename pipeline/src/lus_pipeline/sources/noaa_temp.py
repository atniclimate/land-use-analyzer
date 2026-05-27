"""NOAA NCEI Climate at a Glance temperature trend. See DATA_SOURCES.md section 3.

County-level temperature time series. We compute the trend (degrees F per decade,
1970 to present) for the drought-and-changing-seasons composite. Phase 1c.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "noaa_temp"
PHASE = "1c"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
