"""Building-permit source modules, one per jurisdiction. See DATA_SOURCES.md section 5.

Each module fetches its jurisdiction's permits and harmonizes to the common schema:
permit_id, jurisdiction, parcel_id (best-effort), permit_type, status, issued_date,
valuation, lat, lon. Coverage is surfaced in the UI; we do not pretend to have data
we do not have. Birch Bay is unincorporated and falls under Whatcom County permits.
"""
