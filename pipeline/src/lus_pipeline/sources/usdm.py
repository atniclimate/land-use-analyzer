"""US Drought Monitor (USDM). See DATA_SOURCES.md section 3.

Weekly drought category (D0-D4) at sub-county resolution. We compute the 10-year
frequency of D2+ weeks for the drought composite. Phase 1c.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "usdm"
PHASE = "1c"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
