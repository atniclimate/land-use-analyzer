"""Classification tests proving the editorial intent (PHASE_PLAN 1a checkpoint).

Each fixture row carries a real ``sale_date_1`` so the 30-year tenure gate is exercised
against known dates rather than the placeholder fallback. Today is treated as 2026.
"""

from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from lus_pipeline.classify import OwnershipCategory, classify_parcels
from lus_pipeline.config import load_config

# Sale years relative to the 2026 "today": under 30 years is recent, 30+ established.
RECENT = "2020-05-01"
OLD = "1985-05-01"

# prop_id -> short master row. Mailing address drives concentration clustering.
ROWS: dict[str, dict[str, str]] = {
    # Foreign owner, established (41 years): stays neutral.
    "1": {
        "owner": "PIERRE TREMBLAY",
        "state": "BC",
        "country": "CAN",
        "addr": "1 RUE A",
        "sale": OLD,
    },
    # Foreign owner, recent: flagged Foreign.
    "2": {
        "owner": "AKIRA SATO",
        "state": "",
        "country": "JAPAN",
        "addr": "2 CHOME B",
        "sale": RECENT,
    },
    # Out-of-state owner, recent: flagged Out-of-State.
    "3": {
        "owner": "JANE MILLER",
        "state": "OR",
        "country": "",
        "addr": "3 PINE ST",
        "sale": RECENT,
    },
    # Out-of-state owner, established: neutral.
    "4": {"owner": "TOM HALE", "state": "CA", "country": "", "addr": "4 OAK AVE", "sale": OLD},
    # Family LLC, single homestead: Small Corporate, not concentrated, not flagged.
    "5": {
        "owner": "SMITH FAMILY LLC",
        "state": "WA",
        "country": "",
        "addr": "5 FARM RD",
        "sale": RECENT,
    },
    # Concentrated cluster: three recent parcels at one mailing address.
    "10": {
        "owner": "ACME HOLDINGS LLC",
        "state": "WA",
        "country": "",
        "addr": "100 FUND ST",
        "sale": RECENT,
    },
    "11": {
        "owner": "ACME HOLDINGS LLC",
        "state": "WA",
        "country": "",
        "addr": "100 FUND ST",
        "sale": RECENT,
    },
    "12": {
        "owner": "ACME HOLDINGS LLC",
        "state": "WA",
        "country": "",
        "addr": "100 FUND ST",
        "sale": RECENT,
    },
    # Older member of the same cluster: stays neutral (the cluster gradient).
    "13": {
        "owner": "ACME HOLDINGS LLC",
        "state": "WA",
        "country": "",
        "addr": "100 FUND ST",
        "sale": OLD,
    },
    # Government, even with a recent sale: never corporate.
    "20": {
        "owner": "CITY OF BELLINGHAM",
        "state": "WA",
        "country": "",
        "addr": "210 LOTTIE ST",
        "sale": RECENT,
    },
    # Tribal trust via exemption subtype.
    "21": {
        "owner": "UNITED STATES DEPT OF INTERIOR BIA",
        "state": "OR",
        "country": "",
        "addr": "911 NE 11TH",
        "sale": RECENT,
        "exmpt": "INDIAN",
    },
    # Plain local individual.
    "30": {
        "owner": "MARIA LOPEZ",
        "state": "WA",
        "country": "",
        "addr": "30 ELM ST",
        "sale": RECENT,
    },
}


def _build() -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    sm_records = []
    parcel_records = []
    for i, (pid, r) in enumerate(ROWS.items()):
        sm_records.append(
            {
                "prop_id": pid,
                "geo_id": pid.zfill(16),
                "title_owner_name_full": r["owner"],
                "title_owner_city": "ANYWHERE",
                "title_owner_state": r["state"],
                "title_owner_country": r["country"],
                "title_owner_add_full": r["addr"],
                "exmpt_subtype_cd": r.get("exmpt", ""),
                "legal_acreage": "1.0",
                "appraised_val_total": "100000",
                "sale_date_1": r["sale"],
            }
        )
        parcel_records.append(
            {"Prop_ID": int(pid), "WCAGCODE": pid.zfill(16), "geometry": box(i, 0, i + 1, 1)}
        )
    short_master = pd.DataFrame(sm_records)
    parcels = gpd.GeoDataFrame(parcel_records, geometry="geometry", crs="EPSG:4326")
    return parcels, short_master


def _classified() -> gpd.GeoDataFrame:
    parcels, short_master = _build()
    result = classify_parcels(parcels, short_master, load_config())
    return result.set_index("prop_id")


def test_tenure_source_is_real_when_sale_date_present() -> None:
    assert (_classified()["tenure_source"] == "assessor").all()


def test_foreign_established_stays_neutral() -> None:
    row = _classified().loc["1"]
    assert row["ownership_category"] == OwnershipCategory.LOCAL
    assert not row["flagged"]


def test_foreign_recent_is_flagged() -> None:
    row = _classified().loc["2"]
    assert row["ownership_category"] == OwnershipCategory.FOREIGN
    assert row["flagged"]


def test_out_of_state_recent_is_flagged() -> None:
    row = _classified().loc["3"]
    assert row["ownership_category"] == OwnershipCategory.OUT_OF_STATE
    assert row["flagged"]


def test_out_of_state_established_stays_neutral() -> None:
    row = _classified().loc["4"]
    assert row["ownership_category"] == OwnershipCategory.LOCAL
    assert not row["flagged"]


def test_family_llc_is_small_not_concentrated() -> None:
    row = _classified().loc["5"]
    assert row["ownership_category"] == OwnershipCategory.SMALL_CORPORATE
    assert not row["flagged"]


def test_concentrated_cluster_recent_members_flagged() -> None:
    result = _classified()
    for pid in ("10", "11", "12"):
        assert result.loc[pid, "ownership_category"] == OwnershipCategory.CONCENTRATED_CORPORATE
        assert result.loc[pid, "flagged"]


def test_concentrated_cluster_old_member_stays_neutral() -> None:
    row = _classified().loc["13"]
    assert row["ownership_category"] == OwnershipCategory.LOCAL
    assert not row["flagged"]


def test_government_never_corporate() -> None:
    row = _classified().loc["20"]
    assert row["ownership_category"] == OwnershipCategory.GOVERNMENT_TRIBAL_UTILITY
    assert not row["flagged"]


def test_tribal_trust_exemption_is_government() -> None:
    row = _classified().loc["21"]
    assert row["ownership_category"] == OwnershipCategory.GOVERNMENT_TRIBAL_UTILITY
    assert not row["flagged"]


def test_local_individual_is_neutral() -> None:
    row = _classified().loc["30"]
    assert row["ownership_category"] == OwnershipCategory.LOCAL
    assert not row["flagged"]
