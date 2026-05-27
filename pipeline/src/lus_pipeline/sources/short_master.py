"""Whatcom County Property Short Master. See DATA_SOURCES.md section 1.

Tabular owner names, mailing addresses, acreage, assessed values, and sale dates.
`sale_date_1` (or equivalent) is the primary tenure input and is central to
classification, not just the changing-hands view. Column names shift across
releases; detect them rather than hard-coding. Phase 1a.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "short_master"
PHASE = "1a"


def fetch(config: Config) -> Path:
    raise NotImplementedError(f"{NAME}.fetch is a Phase {PHASE} task.")


def load(config: Config):
    raise NotImplementedError(f"{NAME}.load is a Phase {PHASE} task.")
