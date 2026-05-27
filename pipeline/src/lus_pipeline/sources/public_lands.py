"""Public lands context layers. See DATA_SOURCES.md section 6.

USFS, NPS, USFWS, BLM, WA DNR, WA State Parks, and WDFW boundaries. Toggle-able
context layers in explore mode, not story views. Phase 1f.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "public_lands"
PHASE = "1f"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
