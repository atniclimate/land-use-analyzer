"""Sales velocity and ownership change. See DATA_SOURCES.md section 4.

Per-parcel tenure plus neighborhood sales density (sales within a 1km buffer,
current 24 months vs. prior 24 months) and cluster-growth signal. Tenure inputs
overlap with classification (short master, REET, Auditor). Baseline year 1970. Phase 1d.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "sales_velocity"
PHASE = "1d"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
