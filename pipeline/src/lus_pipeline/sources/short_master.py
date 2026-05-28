"""Whatcom County Property Short Master. See DATA_SOURCES.md section 1.

Tabular owner names, mailing addresses, acreage, assessed values, and sale dates,
keyed by the 16-digit GID. `sale_date_1` (or equivalent) is the primary tenure input
and is central to classification, not just the changing-hands view. Column names
shift across releases, so detect them rather than hard-coding (see classify.py).
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
import pandas as pd

if TYPE_CHECKING:
    from lus_pipeline.config import Config

NAME = "short_master"
PHASE = "1a"
_ARCHIVE = "short_master.zip"


def fetch(config: Config) -> Path:
    """Download the short master CSV archive to raw_dir. Returns the written path."""
    config.ensure_dirs()
    dest = config.raw_dir / _ARCHIVE
    with httpx.Client(follow_redirects=True, timeout=120.0) as client:
        resp = client.get(config.sources.short_master_csv)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
    return dest


def load(config: Config) -> pd.DataFrame:
    """Read the short master as a DataFrame of strings (cast specific columns later)."""
    archive = config.raw_dir / _ARCHIVE
    if not archive.exists():
        raise FileNotFoundError(f"{archive} not found. Run short_master.fetch() first.")
    with zipfile.ZipFile(archive) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise ValueError(f"No CSV found in {archive}: {zf.namelist()}")
        data = zf.read(csv_names[0])
    return pd.read_csv(io.BytesIO(data), dtype=str, encoding="latin-1", low_memory=False)
