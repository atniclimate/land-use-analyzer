"""Tribal trust land context layer. See DATA_SOURCES.md section 7.

BIA Indian Lands GIS federal trust parcels. Displayed as a quiet context layer with
the lightest possible styling. For v1 we do NOT display reservation boundaries as a
primary layer, and we do NOT display treaty or usual-and-accustomed areas; that work
is deferred to a future consultation-led version. Phase 1f.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "tribal_trust"
PHASE = "1f"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
