"""Ownership classification.

Implements the tenure-gated, first-match-wins hierarchy in CLAUDE.md. Categories are
computed from the real assessor data (owner name, mailing state/country, corporate
tokens, concentration clusters). The 30-year tenure gate needs a sale date.

The Whatcom short master and public REST layer do not currently expose a sale date
(verified 2026-05), so when no sale-date column is present we fall back to a clearly
labeled PLACEHOLDER tenure (deterministic per parcel). `tenure_source` records which
was used so the UI can warn that recency is demo data. When a real sale-date column
appears, `compute_tenure` uses it automatically and the gate becomes real.
"""

from __future__ import annotations

import re
import zlib
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING

import geopandas as gpd
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from lus_pipeline.config import Config


class OwnershipCategory(StrEnum):
    """First-match-wins hierarchy. Order matters: the first matching rule wins."""

    GOVERNMENT_TRIBAL_UTILITY = "government_tribal_utility"
    CONCENTRATED_CORPORATE = "concentrated_corporate"
    SMALL_CORPORATE = "small_corporate"
    OUT_OF_STATE = "out_of_state"
    FOREIGN = "foreign"
    LOCAL = "local"


# Categories gated by the per-parcel tenure rule. A parcel lands in one of these
# only when the current owner's tenure is under Thresholds.tenure_years (default 30).
# Established owners (30+ years) stay neutral regardless of mailing address.
TENURE_GATED: tuple[OwnershipCategory, ...] = (
    OwnershipCategory.CONCENTRATED_CORPORATE,
    OwnershipCategory.OUT_OF_STATE,
    OwnershipCategory.FOREIGN,
)

US_STATES: frozenset[str] = frozenset(
    {
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
        "DC",
        "PR",
        "GU",
        "VI",
        "AS",
        "MP",
    }
)
OUT_OF_STATE_STATES: frozenset[str] = US_STATES - {"WA"}

# Word-boundary token regexes over normalized (uppercased, punctuation-stripped) names.
_GOV_TOKENS = [
    "UNITED STATES",
    "STATE OF",
    "COUNTY OF",
    "CITY OF",
    "TOWN OF",
    "PORT OF",
    "PORT DISTRICT",
    "PUBLIC UTILITY",
    "PUD",
    "SCHOOL DISTRICT",
    "FIRE DISTRICT",
    "WATER DISTRICT",
    "SEWER DISTRICT",
    "DIKING DISTRICT",
    "DRAINAGE DISTRICT",
    "CEMETERY DISTRICT",
    "PARK DISTRICT",
    "CONSERVATION DISTRICT",
    "HOUSING AUTHORITY",
    "DEPT OF",
    "DEPARTMENT OF",
    "BUREAU OF",
    "DEPT OF INTERIOR",
    "BIA",
    "IN TRUST",
    "TRIBE",
    "TRIBES",
    "TRIBAL",
    "NATION",
    "INDIAN",
    "DNR",
    "FISH AND WILDLIFE",
    "FISH WILDLIFE",
    "WSDOT",
    "BONNEVILLE",
    "ARMY CORPS",
    "CORPS OF ENGINEERS",
    "STATE PARKS",
    "UNIVERSITY",
    "COLLEGE",
    "LIBRARY",
    "WHATCOM COUNTY",
    "METRO",
]
_CORP_TOKENS = [
    "LLC",
    "L L C",
    "INC",
    "INCORPORATED",
    "CORP",
    "CORPORATION",
    "COMPANY",
    "LP",
    "LLP",
    "LTD",
    "LIMITED",
    "TRUST",
    "PARTNERS",
    "PARTNERSHIP",
    "HOLDINGS",
    "PROPERTIES",
    "INVESTMENTS",
    "CAPITAL",
    "GROUP",
    "ENTERPRISES",
    "VENTURES",
    "ASSOCIATES",
    "REALTY",
    "DEVELOPMENT",
    "MANAGEMENT",
    "FUND",
    "EQUITY",
    "BANK",
    "FINANCIAL",
]
_GOV_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in _GOV_TOKENS) + r")\b")
_CORP_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in _CORP_TOKENS) + r")\b")
_NON_ALNUM = re.compile(r"[^A-Z0-9]+")
_US_COUNTRY_TOKENS = frozenset({"", "USA", "US", "U S", "UNITED STATES"})

# Candidate column names for a sale-date column, checked case-insensitively.
_SALE_DATE_CANDIDATES = ("sale_date_1", "sale_date", "saledate", "sale_dt", "deed_date")


def normalize_text(value: object) -> str:
    """Uppercase, strip punctuation, collapse whitespace. Empty for missing values."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    text = _NON_ALNUM.sub(" ", str(value).upper())
    return " ".join(text.split())


def detect_column(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    """Return the first column whose lowercased name matches a candidate, else None."""
    lower = {c.lower(): c for c in columns}
    for candidate in candidates:
        if candidate in lower:
            return lower[candidate]
    return None


def compute_tenure(df: pd.DataFrame, config: Config) -> tuple[pd.Series, str]:
    """Return (tenure_years, source). Uses a real sale-date column if present.

    Real source: tenure is years since the most recent sale. Missing or pre-baseline
    sale dates are long-established (NaN tenure, never flagged). Placeholder source:
    a deterministic per-parcel value so the gate and map can be demonstrated.
    """
    sale_col = detect_column(list(df.columns), _SALE_DATE_CANDIDATES)
    if sale_col is not None:
        parsed = pd.to_datetime(df[sale_col], errors="coerce")
        year = parsed.dt.year
        long_established = year.isna() | (year < config.thresholds.sales_baseline_year)
        tenure = float(date.today().year) - year
        tenure = tenure.mask(long_established, other=np.nan)
        return tenure, "assessor"

    span = float(date.today().year - config.thresholds.sales_baseline_year)
    placeholder = (
        df["prop_id"].astype(str).map(lambda s: zlib.crc32(s.encode()) % int(span)).astype(float)
    )
    return placeholder, "placeholder"


def _is_concentrated(
    norm_addr: pd.Series, corp_mask: pd.Series, acres: pd.Series, value: pd.Series, config: Config
) -> pd.Series:
    """Per-parcel boolean: is this corporate parcel part of a concentrated cluster?

    Cluster key is the normalized owner mailing address, among corporate owners only.
    A cluster is concentrated if it meets ANY threshold (parcels, acres, or value).
    """
    thresholds = config.thresholds.concentration
    corp = corp_mask & norm_addr.ne("")
    cluster = pd.DataFrame(
        {"key": norm_addr[corp], "acres": acres[corp].fillna(0.0), "value": value[corp].fillna(0.0)}
    )
    grouped = cluster.groupby("key").agg(
        n=("key", "size"), acres=("acres", "sum"), value=("value", "sum")
    )
    concentrated = grouped[
        (grouped["n"] >= thresholds.min_parcels)
        | (grouped["acres"] >= thresholds.min_total_acres)
        | (grouped["value"] >= thresholds.min_total_assessed_value)
    ].index
    return corp & norm_addr.isin(concentrated)


def classify_parcels(
    parcels: gpd.GeoDataFrame, short_master: pd.DataFrame, config: Config
) -> gpd.GeoDataFrame:
    """Join parcels to the short master and assign the tenure-gated ownership category.

    Returns a GeoDataFrame with display fields plus `ownership_category`,
    `tenure_years`, `tenure_source`, and `flagged`. See CLAUDE.md, "Classification
    thresholds", and PHASE_PLAN.md section 1a.
    """
    sm = short_master.copy()
    sm["prop_id"] = sm["prop_id"].astype(str).str.strip()
    parcels = parcels.copy()
    parcels["prop_id"] = parcels["Prop_ID"].astype(str).str.strip()
    merged = parcels.merge(sm, on="prop_id", how="left", suffixes=("", "_sm"))

    owner = merged["title_owner_name_full"].fillna("").map(normalize_text)
    state = merged["title_owner_state"].fillna("").str.strip().str.upper()
    country = merged["title_owner_country"].fillna("").str.strip().str.upper()
    exmpt = merged["exmpt_subtype_cd"].fillna("").str.strip().str.upper()
    acres = pd.to_numeric(merged["legal_acreage"], errors="coerce")
    value = pd.to_numeric(merged["appraised_val_total"], errors="coerce")
    norm_addr = merged["title_owner_add_full"].map(normalize_text)

    is_gov = owner.str.contains(_GOV_RE) | exmpt.eq("INDIAN")
    has_corp = owner.str.contains(_CORP_RE)
    is_foreign = ~country.isin(_US_COUNTRY_TOKENS)
    is_out_of_state = state.isin(OUT_OF_STATE_STATES)
    is_concentrated = _is_concentrated(norm_addr, has_corp & ~is_gov, acres, value, config)

    # Raw mailing pattern, independent of corporate and tenure. The UI uses this to
    # give established out-of-state and out-of-country owners a muted but visible
    # background tint (rule #2 from CLAUDE.md, refined: "neutral" becomes a gradient).
    mailing_signal = pd.Series(
        np.select(
            [is_out_of_state, is_foreign, state.eq("WA")],
            ["out_of_state", "foreign", "wa"],
            default="unknown",
        ),
        index=merged.index,
    )

    tenure_years, tenure_source = compute_tenure(merged, config)
    recent = tenure_years.lt(config.thresholds.tenure_years).fillna(False)

    conditions = [
        is_gov,
        has_corp & is_concentrated & recent,
        has_corp & ~is_concentrated,
        is_out_of_state & recent,
        is_foreign & recent,
    ]
    choices = [
        OwnershipCategory.GOVERNMENT_TRIBAL_UTILITY.value,
        OwnershipCategory.CONCENTRATED_CORPORATE.value,
        OwnershipCategory.SMALL_CORPORATE.value,
        OwnershipCategory.OUT_OF_STATE.value,
        OwnershipCategory.FOREIGN.value,
    ]
    category = pd.Series(
        np.select(conditions, choices, default=OwnershipCategory.LOCAL.value), index=merged.index
    )
    flagged = category.isin([c.value for c in TENURE_GATED])

    result = gpd.GeoDataFrame(
        {
            "prop_id": merged["prop_id"],
            "geo_id": merged.get("geo_id"),
            "owner": merged["title_owner_name_full"].fillna(""),
            "mailing_city": merged["title_owner_city"].fillna(""),
            "mailing_state": state,
            "mailing_country": country,
            "acres": acres.round(2),
            "assessed_value": value,
            "ownership_category": category,
            "mailing_signal": mailing_signal,
            "tenure_years": tenure_years.round(0),
            "tenure_source": tenure_source,
            "flagged": flagged,
        },
        geometry=merged.geometry,
        crs=merged.crs,
    )
    return result
