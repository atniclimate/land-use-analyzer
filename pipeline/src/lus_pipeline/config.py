"""Pipeline configuration: paths and classification/tier thresholds.

Values here are the project defaults documented in CLAUDE.md and DATA_SOURCES.md.
Nothing in this module touches the network.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

# pipeline/src/lus_pipeline/config.py -> parents[2] == pipeline/
PIPELINE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PIPELINE_ROOT.parent


class ConcentrationThresholds(BaseModel):
    """Cluster-level thresholds for the Concentrated Corporate category.

    A cluster is the set of parcels sharing a normalized mailing address and a
    matching corporate-suffix token family. A cluster counts as concentrated when
    it meets ANY of these thresholds. Adjustable via the explore-mode UI slider.
    """

    min_parcels: int = 3
    min_total_acres: float = 50.0
    min_total_assessed_value: float = 2_000_000.0


class Thresholds(BaseModel):
    """Editorial thresholds. See CLAUDE.md, "Classification thresholds"."""

    # Per-parcel tenure gate, applied symmetrically to Foreign, Out-of-State, and
    # Concentrated Corporate. Under this many years: flagged. At or over: neutral.
    tenure_years: int = 30
    # Sale dates earlier than this year (or missing) count as long-established.
    sales_baseline_year: int = 1970
    concentration: ConcentrationThresholds = Field(default_factory=ConcentrationThresholds)


class Config(BaseModel):
    """Resolved pipeline configuration."""

    pipeline_root: Path = PIPELINE_ROOT
    data_dir: Path = PIPELINE_ROOT / "data"
    tiles_output_dir: Path = REPO_ROOT / "webapp" / "public" / "tiles"
    thresholds: Thresholds = Field(default_factory=Thresholds)

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def intermediate_dir(self) -> Path:
        return self.data_dir / "intermediate"

    @property
    def cache_dir(self) -> Path:
        return self.data_dir / "cache"

    def ensure_dirs(self) -> None:
        """Create the data and tile output directories if they do not exist."""
        for path in (self.raw_dir, self.intermediate_dir, self.cache_dir, self.tiles_output_dir):
            path.mkdir(parents=True, exist_ok=True)


def load_config() -> Config:
    """Return the default project configuration."""
    return Config()
