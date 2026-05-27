"""WA Department of Ecology floodplain mapping. See DATA_SOURCES.md section 2.

State-mapped floodplain and channel migration zones, often more current than FEMA
for fast-changing rivers like the Nooksack. Via the WA Geoportal. Phase 1b.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "wa_ecology_flood"
PHASE = "1b"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
