"""Phase 0 smoke tests: the skeleton imports, the vocabulary is intact, the CLI runs.

Real classification tests with fixture data land in Phase 1a (see PHASE_PLAN.md).
"""

from __future__ import annotations

from lus_pipeline import refresh
from lus_pipeline.classify import TENURE_GATED, OwnershipCategory
from lus_pipeline.config import load_config
from lus_pipeline.sources import SOURCE_GROUPS
from lus_pipeline.tier import Tier


def test_ownership_categories() -> None:
    assert len(OwnershipCategory) == 6
    # The three flagged categories are the tenure-gated ones; Local and Government are not.
    assert set(TENURE_GATED) == {
        OwnershipCategory.CONCENTRATED_CORPORATE,
        OwnershipCategory.OUT_OF_STATE,
        OwnershipCategory.FOREIGN,
    }
    assert OwnershipCategory.LOCAL not in TENURE_GATED
    assert OwnershipCategory.GOVERNMENT_TRIBAL_UTILITY not in TENURE_GATED


def test_tiers() -> None:
    assert {t.value for t in Tier} == {"low", "medium", "high"}


def test_config_defaults() -> None:
    config = load_config()
    assert config.thresholds.tenure_years == 30
    assert config.thresholds.sales_baseline_year == 1970
    assert config.thresholds.concentration.min_parcels == 3
    assert config.thresholds.concentration.min_total_acres == 50.0
    assert config.thresholds.concentration.min_total_assessed_value == 2_000_000.0


def test_source_groups_nonempty() -> None:
    assert SOURCE_GROUPS["parcels"]
    assert "short_master" in SOURCE_GROUPS["parcels"]


def test_cli_runs() -> None:
    assert refresh.main(["--dry-run"]) == 0
    assert refresh.main(["--list-sources"]) == 0
