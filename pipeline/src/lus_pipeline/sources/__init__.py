"""Data source modules.

Each source module exposes a `fetch(config)` function that writes to the
intermediate data dir and a `load(config)` function that reads it back as a
(Geo)DataFrame. See DATA_SOURCES.md for the per-source endpoints, licenses, and
refresh cadence.

SOURCE_GROUPS lists every registered source by category. Module names are relative
to this package (lus_pipeline.sources); the orchestrator resolves them lazily.
"""

from __future__ import annotations

SOURCE_GROUPS: dict[str, tuple[str, ...]] = {
    "parcels": ("parcels", "short_master"),
    "flood": ("fema_nfhl", "usgs_inundation", "wa_ecology_flood"),
    "drought": ("usdm", "noaa_temp", "snotel"),
    "sales": ("sales_velocity",),
    "permits": (
        "permits.whatcom_county",
        "permits.bellingham",
        "permits.lynden",
        "permits.ferndale",
        "permits.blaine",
        "permits.sumas",
        "permits.everson",
        "permits.nooksack",
    ),
    "public_lands": ("public_lands",),
    "tribal_trust": ("tribal_trust",),
}
