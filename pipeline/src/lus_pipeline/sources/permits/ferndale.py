"""City of Ferndale permits. See DATA_SOURCES.md section 5. Phase 1e."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "ferndale"
JURISDICTION = "City of Ferndale"
PHASE = "1e"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"permits.{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"permits.{NAME}.load is a Phase {PHASE} task.")
