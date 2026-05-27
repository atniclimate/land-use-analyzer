"""NRCS SNOTEL snowpack. See DATA_SOURCES.md section 3.

April 1 Snow Water Equivalent (SWE) trend at automated sites (Wells Creek, Elbow
Lake, Easy Pass) for the drought composite. Via the AWDB REST service. Phase 1c.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "snotel"
PHASE = "1c"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
