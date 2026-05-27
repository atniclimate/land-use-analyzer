# Data Sources

This file catalogs every public dataset Land Use Analyzer uses. Each entry includes the source, endpoint, license, refresh cadence, and integration notes.

All sources are **public**. None require authentication beyond standard rate limits. The pipeline must handle absent or stale feeds gracefully: if one feed is down, the rest of the build should still succeed.

---

## 1. Parcel & ownership

### Whatcom County Property Short Master
- **What**: Tabular file with parcel numbers, owner names, mailing addresses, acreage, and assessed values.
- **URL**: https://www.whatcomcounty.us/3869/Property-Data-Downloads
- **Formats**: CSV (zip), MDB (zip), XLSX
- **Refresh**: Monthly. The county posts a new file approximately the first of each month.
- **License**: Public record per Washington RCW 42.56. RCW 42.56.070 prohibits commercial-list use; we are not commercial.
- **Pipeline module**: `pipeline/src/lus_pipeline/sources/short_master.py`
- **Notes**: Column names have shifted across releases. Use the auto-detection pattern in `classify.py`.

### Whatcom County GIS Parcel Shapefile
- **What**: Polygon geometry for every tax parcel, attributed with the 16-digit Geographic Identifier (GID).
- **URL**: https://www.whatcomcounty.us/3869/Property-Data-Downloads
- **Format**: Shapefile (zip with 8 related files)
- **Refresh**: Monthly, same cadence as short master.
- **License**: Same disclaimer as short master.
- **Pipeline module**: `pipeline/src/lus_pipeline/sources/parcels.py`
- **Notes**: PID = 0 means no tax account assigned (common parcels, river wash, unknown ownership, Tribal land). The 16-digit GID is the join key to the short master.

### Sale date / tenure data (central classification input)

`sale_date` is **central to classification**, not just to the "changing hands" story view. The 30-year tenure rule in `classify.py` gates Foreign, Out-of-State, and Concentrated Corporate flagging on whether the current owner's tenure is under 30 years. Three layered sources:

1. **Short master `sale_date_1`** (or equivalent column). This is the most recent sale per parcel and is the primary input. The county refreshes it monthly. Use this first.
2. **WA Department of Revenue Real Estate Excise Tax (REET)** for historical depth.
   - **URL**: https://dor.wa.gov/about/statistics-reports/real-estate-excise-tax-statistics (statistics); full data via public records request.
   - **Refresh**: Quarterly summaries; bulk historical data on request.
   - **License**: Public.
   - **Use**: Fallback when short master lacks sale history, and depth back to 1970 for the sales velocity story view.
3. **Whatcom County Auditor / Recorder** for cross-reference.
   - **URL**: https://www.whatcomcounty.us/198/Auditor
   - **Search**: https://recording.whatcomcounty.us
   - **Use**: Verify unusual ownership changes flagged by classification (entity-to-entity transfers, multi-parcel cluster acquisitions).

**Missing-data policy**: If `sale_date` is missing or earlier than 1970, treat the parcel as **long-established**. Do not flag. This is conservative by design; the rule preferences "neighbor we don't know about" over "false flag."

**Known limitation**: Entity-to-entity transfers (family LLC to successor family LLC, parent-to-child via LLC vehicle) show as recent sales and will trigger the flag even when underlying ownership is multigenerational. Document this on the methodology page and provide a correction-report contact.

---

## 2. Flood

The flood layer **combines three sources**. None alone is sufficient.

### FEMA National Flood Hazard Layer (NFHL)
- **What**: Regulatory flood zone designations (AE, A, VE, X, etc.).
- **URL**: https://hazards.fema.gov/femaportal/NFHL/searchResult
- **API**: NFHL is served via ArcGIS REST: https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer
- **Format**: GeoJSON via ArcGIS query; shapefile bulk download by county.
- **Refresh**: Updated by FEMA periodically; check semi-annually.
- **License**: Public domain (US federal).
- **Pipeline module**: `pipeline/src/lus_pipeline/sources/fema_nfhl.py`

### USGS Flood Inundation Mapper
- **What**: Modeled inundation extents at various stream stages, gauged to specific streamgages.
- **URL**: https://fim.wim.usgs.gov/fim/
- **API**: REST: https://stn.wim.usgs.gov/STNServices/Sites.json (sites); inundation polygons by gauge.
- **Refresh**: Updated as new models are developed.
- **License**: Public domain (US federal).
- **Coverage**: Not all Whatcom streams are gauged. The Nooksack is reasonably covered.
- **Pipeline module**: `pipeline/src/lus_pipeline/sources/usgs_inundation.py`

### NOAA Advanced Hydrologic Prediction Service (AHPS)
- **What**: Stream gauge data, flood thresholds (action, minor, moderate, major), recent crests.
- **URL**: https://water.weather.gov/ahps/
- **API**: Per-gauge XML/JSON.
- **Refresh**: Real-time, but we snapshot monthly.
- **License**: Public domain (US federal).
- **Use**: Inform the "recent gauged event" condition in High tier classification.

### WA Department of Ecology: Floodplain Mapping
- **What**: State-mapped floodplain and channel migration zones, often more current than FEMA in fast-changing rivers like the Nooksack.
- **URL**: https://ecology.wa.gov/Water-Shorelines/Shoreline-coastal-management/Hazards/Floods-floodplain-planning
- **Data portal**: https://geo.wa.gov (search "flood")
- **Format**: Shapefile / GeoJSON via WA Geoportal.
- **License**: Public.
- **Pipeline module**: `pipeline/src/lus_pipeline/sources/wa_ecology_flood.py`

### Whatcom County Flood Models (post-November 2021)
- **What**: County-commissioned Nooksack basin hydraulic modeling done after the November 2021 flood.
- **URL**: https://www.whatcomcounty.us/2828/River-Flood-Warning-System (entry point; specific model outputs are linked or available on request)
- **Refresh**: Updated as models are revised.
- **License**: Public.
- **Notes**: This is the most locally-accurate dataset for the Nooksack basin. Prioritize where coverage exists.

---

## 3. Drought & changing seasons

### US Drought Monitor (USDM)
- **What**: Weekly drought category map (D0–D4) at sub-county resolution.
- **URL**: https://droughtmonitor.unl.edu/
- **API**: GIS shapefiles by week: https://droughtmonitor.unl.edu/DmData/GISData.aspx
- **Refresh**: Weekly. We aggregate to monthly for display, but compute the historical 10-year frequency.
- **License**: Public.
- **Pipeline module**: `pipeline/src/lus_pipeline/sources/usdm.py`

### NOAA-NIDIS (drought.gov)
- **What**: Integrated drought indicators, outlooks, regional summaries.
- **URL**: https://www.drought.gov/states/washington/county/whatcom
- **API**: Various; see https://www.drought.gov/api
- **Refresh**: Weekly to monthly.
- **License**: Public domain (US federal).

### NOAA NCEI Climate at a Glance
- **What**: County-level temperature and precipitation time series.
- **URL**: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/county/time-series
- **API**: JSON: https://www.ncei.noaa.gov/access/services/data/v1
- **Refresh**: Monthly.
- **License**: Public domain (US federal).
- **Use**: Compute temperature trend (degrees F per decade, 1970–present) for the drought-and-changing-seasons composite.

### NRCS SNOTEL
- **What**: Mountain snowpack measurements at automated sites.
- **URL**: https://www.nrcs.usda.gov/wps/portal/wcc/home/snowClimateMonitoring/snowpack/
- **API**: AWDB REST.
- **Relevant sites**: Wells Creek, Elbow Lake, Easy Pass (upper Nooksack and surrounding).
- **License**: Public domain (US federal).
- **Use**: April 1 Snow Water Equivalent (SWE) trend for the composite.

### NOAA Climate Prediction Center (CPC) Seasonal Outlooks
- **What**: 1-month and 3-month temperature, precipitation, and drought outlooks.
- **URL**: https://www.cpc.ncep.noaa.gov/
- **License**: Public domain (US federal).
- **Use**: Short-term outlook text on the drought story view. **Do not** use for spatially-resolved tier assignment.

---

## 4. Sales velocity & ownership change

The data inputs for this story view and for the tenure-gated classification overlap completely. See **"Sale date / tenure data"** in section 1 above for the three layered sources (short master, REET, Auditor/Recorder).

**Story-view-specific computations** (in addition to per-parcel tenure used by classification):

- **Sales-per-area-per-time**: count of sales within a rolling 1km buffer, current 24 months vs. prior 24 months. Computed in `pipeline/src/lus_pipeline/sources/sales_velocity.py`.
- **Cluster-growth signal**: for each Concentrated Corporate cluster, count parcels acquired in the past 24 months. Drives the cluster size visualization in the story view.
- **Sales velocity baseline**: 1970 (Washington opened to unrestricted foreign ownership shortly after this date).

---

## 5. Building activity (permits)

This is the most fragmented data category. Each jurisdiction below issues its own permits.

### Whatcom County permits (unincorporated areas)
- **URL**: https://permits.whatcomcounty.us/CitizenAccess/
- **Refresh**: Monthly snapshot.

### City of Bellingham
- **URL**: https://cob.org/services/business/development-services
- **Permit portal**: https://aca-prod.accela.com/BELLINGHAM/
- **Notes**: Largest population center; most permit activity.

### City of Lynden
- **URL**: https://www.lyndenwa.org/government/planning_community_development/
- **Refresh**: Check monthly.

### City of Ferndale
- **URL**: https://www.cityofferndale.org/community-development/

### City of Blaine
- **URL**: https://www.cityofblaine.com/189/Community-Development

### City of Sumas
- **URL**: https://cityofsumas.com/

### City of Everson
- **URL**: https://www.eversonwa.gov/

### City of Nooksack
- **URL**: https://nooksackcity.com/

### Birch Bay
- **Notes**: Unincorporated; falls under Whatcom County permits but distinct community of interest. Surface separately in UI if data supports it.

### Pipeline approach for permits
- One source module per jurisdiction in `pipeline/src/lus_pipeline/sources/permits/`.
- Harmonize to a common schema: `permit_id, jurisdiction, parcel_id (best-effort), permit_type, status, issued_date, valuation, lat, lon`.
- Surface jurisdictional coverage in the UI; do not pretend to have data we don't have.

---

## 6. Public lands (context layers)

### USFS administrative boundaries
- **What**: National Forest boundaries (Mt Baker-Snoqualmie covers much of Whatcom's east).
- **URL**: https://data.fs.usda.gov/geodata/edw/datasets.php
- **Format**: Shapefile / GeoJSON.
- **License**: Public domain.

### National Park Service unit boundaries
- **What**: Whatcom touches North Cascades National Park.
- **URL**: https://public-nps.opendata.arcgis.com/
- **License**: Public domain.

### USFWS National Wildlife Refuge boundaries
- **URL**: https://gis-fws.opendata.arcgis.com/

### BLM Surface Management Agency
- **URL**: https://gbp-blm-egis.hub.arcgis.com/
- **Coverage**: Minimal in Whatcom but include for completeness.

### WA DNR Forest Trust Lands
- **URL**: https://www.dnr.wa.gov/programs-and-services/forest-resources/forest-management/state-trust-lands
- **Data**: https://geo.wa.gov/datasets/wa-dnr::dnr-managed-land-parcels/about
- **License**: Public.

### WA State Parks
- **URL**: https://geo.wa.gov (search "state parks")

### WA Department of Fish & Wildlife: Wildlife Areas
- **URL**: https://wdfw.wa.gov/places-to-go/wildlife-areas
- **Data**: https://geo.wa.gov

---

## 7. Tribal trust land (context layer, minimal styling)

### BIA Indian Lands GIS
- **What**: Federal trust land parcels, reservation boundaries.
- **URL**: https://biamaps.geoplatform.gov/
- **License**: Public domain (US federal).
- **Use**: Display trust land only. **Do not** display reservation boundaries as a primary layer for v1. Do not display treaty or usual-and-accustomed area boundaries; those are deferred to a future consultation-led version.
- **Styling**: Subtle context layer (light fill, no bold outline). The story views do not center this layer.

---

## 8. Base map & reference

### CartoDB Positron (or similar light basemap)
- **URL**: https://carto.com/basemaps/
- **License**: Free for use with attribution.
- **Alternative**: OpenStreetMap raster or vector tiles.

### Whatcom County boundary
- **URL**: https://geo.wa.gov
- **Use**: Clipping mask for tile generation.

### Whatcom municipalities
- **URL**: https://geo.wa.gov
- **Use**: City-name labels and permit-coverage indicators.

---

## Refresh schedule summary

| Source | Cadence | Manual or auto |
|--------|---------|----------------|
| Whatcom parcels + short master | Monthly | Manual |
| FEMA NFHL | Semi-annual check | Manual |
| USGS inundation | As-published check | Manual |
| WA Ecology flood | Quarterly check | Manual |
| US Drought Monitor | Monthly | Manual |
| NOAA temperature | Monthly | Manual |
| NRCS SNOTEL | Monthly (during snow season) | Manual |
| Permits (each jurisdiction) | Monthly | Manual |
| Public lands | Annual check | Manual |
| Tribal trust | Annual check | Manual |

A single `pipeline/scripts/refresh.sh` runs all of these in sequence. Failures in any one source do not block the others.

## Provenance trail

Every layer rendered on the map has a "Source" link in its legend / methodology page. The link goes to the agency portal listed above, not to our internal pipeline. The methodology page lists the date of the local snapshot.
