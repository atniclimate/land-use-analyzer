"""FEMA National Flood Hazard Layer (NFHL). See DATA_SOURCES.md section 2.

Regulatory flood zone designations (AE, A, VE, X, etc.) via the ArcGIS REST
service. One of three flood sources; none alone is sufficient. Phase 1b.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "fema_nfhl"
PHASE = "1b"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
