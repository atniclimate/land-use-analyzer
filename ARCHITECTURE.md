# Architecture

This document explains the technical choices behind Land Use Analyzer. It is written for collaborators and contributors. End-user content lives in the README and the in-app methodology pages.

---

## Big picture

```
┌──────────────────────┐         ┌────────────────────────────┐
│   Public agency      │         │   Land Use Analyzer repo   │
│   data sources       │ ──────▶ │    pipeline/  (Python)     │
│   (FEMA, USGS, WA    │         │                            │
│   Ecology, NOAA,     │         │  fetch → classify →        │
│   Whatcom County,    │         │  tier → tile               │
│   etc.)              │         │                            │
└──────────────────────┘         └─────────────┬──────────────┘
                                               │ commits
                                               ▼
                                 ┌────────────────────────────┐
                                 │    webapp/public/tiles/    │
                                 │    *.pmtiles               │
                                 └─────────────┬──────────────┘
                                               │ static fetch
                                               ▼
                                 ┌────────────────────────────┐
                                 │    webapp/  (TypeScript)   │
                                 │    Vite + React +          │
                                 │    MapLibre + deck.gl      │
                                 └─────────────┬──────────────┘
                                               │ deploy
                                               ▼
                                 ┌────────────────────────────┐
                                 │    Static hosting          │
                                 │    (GitHub Pages for demo) │
                                 └────────────────────────────┘
```

Two halves: a **Python pipeline** that runs on the maintainer's machine to fetch public data and produce vector tiles, and a **TypeScript web app** that renders those tiles in a browser. The two halves are decoupled: the pipeline writes PMTiles to a known location, the app reads them. No backend server, no live API calls from the browser.

## Why this shape

- **Static hosting** is the cheapest, most resilient deployment model. No server to patch, no database to back up, no API budget to blow.
- **PMTiles** is a single-file vector tile format that serves from any HTTP host (GitHub Pages, S3, Cloudflare R2) via HTTP range requests. No tile server needed.
- **Decoupled pipeline** means the data work is portable. The pipeline can run on the maintainer's laptop, on a CI runner, or on a future server. The web app doesn't care.
- **TypeScript strict mode** in the web app catches a class of bugs at compile time that would otherwise hit production. Stability is an explicit project value.
- **Vector tiles, not raster** because parcels are vector data and users want to click them.

## Web app

### Stack
- **Vite** for the build tool. Fast dev server, sensible defaults.
- **React** 18+ with **TypeScript** strict mode.
- **MapLibre GL JS** for the base map. Open source MapBox fork.
- **deck.gl** for parcel rendering. Handles 200,000+ polygons interactively.
- **Tailwind CSS** for styling. Plays nicely with shadcn/ui.
- **shadcn/ui** for components (Card, Button, Sheet, Slider, etc.).
- **TanStack Router** or React Router for the route tree.
- **Zod** for runtime validation of any external JSON (tile manifests, configs).
- **html-to-image** for the PNG export.

### Route tree
- `/`: landing, choose-your-story-view
- `/flood`: flood story view
- `/drought`: drought & changing seasons
- `/changing-hands`: sales velocity & ownership concentration
- `/building`: permit activity
- `/explore`: layer-toggle mode for power users
- `/print/:view`: fixed-layout render target for PNG export
- `/methodology/:topic`: methodology pages per layer
- `/about`: about the project

### State management
- Per-route state is local (useState/useReducer).
- Map state (center, zoom, selected parcel) lives in a URL-synced store so a user can share a link to a specific view.
- No Redux. No global app state library.

### Map rendering
- MapLibre handles the base map (CartoDB Positron or OpenStreetMap vector).
- deck.gl `MVTLayer` or custom `GeoJsonLayer` reading from PMTiles via the `pmtiles` JS library.
- Parcel styling computed per feature based on the active story view.
- Hover and click handlers attached to deck.gl layers.

### Export
- The print view (`/print/:view`) renders a fixed-aspect layout (e.g., 1600×1000) with map, legend, title, scale bar, north arrow, and attribution. `html-to-image` captures the DOM to PNG.
- The PNG includes the data-current-as-of date and the source attribution.

## Pipeline

### Stack
- **Python 3.11+** managed with **uv** (fast, reproducible).
- **geopandas** + **shapely** + **pyproj** for spatial.
- **duckdb** with the spatial extension for fast joins. Surprisingly efficient for ~80k Whatcom parcels.
- **pandas** for tabular work.
- **httpx** for fetching.
- **pydantic** for config and data validation.
- **tippecanoe** (external binary, installed separately) for vector tile generation.
- **pmtiles** CLI for MBTiles → PMTiles conversion.

### Module layout
```
pipeline/src/lus_pipeline/
├── config.py              # paths, thresholds, source URLs
├── sources/
│   ├── short_master.py
│   ├── parcels.py
│   ├── fema_nfhl.py
│   ├── usgs_inundation.py
│   ├── wa_ecology_flood.py
│   ├── usdm.py
│   ├── noaa_temp.py
│   ├── snotel.py
│   ├── permits/
│   │   ├── whatcom_county.py
│   │   ├── bellingham.py
│   │   └── ... (one per jurisdiction)
│   ├── public_lands.py
│   └── tribal_trust.py
├── classify.py            # ownership classification
├── tier.py                # vulnerability tier assignment
├── tiles.py               # tippecanoe wrapper, PMTiles conversion
└── refresh.py             # orchestrator: fetch → classify → tier → tile
```

Each source module exposes a single `fetch()` function that writes to a known intermediate location (`pipeline/data/intermediate/`), and a `load()` function that reads it back as a GeoDataFrame. The orchestrator handles dependencies and failures.

### Tile generation
- For each story view, generate a separate PMTiles file with only the layers that view needs.
- Use tippecanoe's `--coalesce-densest-as-needed` and `--extend-zooms-if-still-dropping` to keep file sizes reasonable.
- Target file size: under 100 MB per story view. Whatcom is small enough this is achievable.
- Tiles for the parcel base layer are shared across views; story-specific styling is computed client-side from per-feature properties.

### Refresh workflow
```bash
cd pipeline
uv sync
./scripts/refresh.sh
# Outputs land in webapp/public/tiles/
cd ../webapp
pnpm build
# Commit the updated tiles + build output
```

A future enhancement: a GitHub Action that runs the pipeline on a schedule. Not in v1.

## Deployment

### Demo (GitHub Pages)
- The repo has a `gh-pages` branch that GitHub Pages serves from.
- A `pnpm run deploy:gh-pages` script builds the webapp and pushes to that branch.
- The demo URL is the repo's GitHub Pages URL.

### Production
- TBD. Options include Cloudflare Pages, Netlify, or simple static hosting.
- The build output (`webapp/dist/`) is portable; any static host works.

## Performance budget

- Initial page load: under **3 seconds** on a typical broadband connection.
- Time to interactive map: under **5 seconds**.
- PMTiles total payload per story view: under **100 MB** (cached aggressively after first load).
- Parcel rendering: smooth pan/zoom with all of Whatcom County in view (~80k parcels).

## Accessibility & inclusion

- WCAG 2.1 AA target.
- Color is supplemented with patterns or text labels for every classification.
- Keyboard navigation works for all interactive controls (map pan/zoom, story-view switching, parcel selection).
- Screen reader: the map exposes ARIA roles; non-map UI is fully accessible.
- Reading level: 8th grade (see VOICE_GUIDE.md).

## Privacy

- No analytics. No tracking. No cookies beyond what's strictly necessary for routing.
- No user accounts.
- No personal data collected.
- The footer states this plainly.

## Browser support

- Latest two versions of Chrome, Firefox, Safari, Edge.
- No IE.
- Mobile Safari and Chrome on Android work for casual viewing; full-feature use assumes a tablet or larger.

## Open architecture decisions

- **License**: PolyForm Noncommercial 1.0.0. See `LICENSE.md`. The license permits use by individuals, charities, educational institutions, public research organizations, environmental protection organizations, and government institutions. It prohibits commercial use, sublicensing, or transfer of license rights. This is a deliberate choice that values controlled distribution over maximum adoption; people can use the tool, but cannot fork, modify, or redistribute it without explicit permission.
- **Hosting**: GitHub Pages for demo is confirmed. Production host is TBD.
- **Domain**: own domain or GitHub Pages URL?
- **CI**: GitHub Actions for linting and type-checking on pull requests. The pipeline itself stays manual for v1.
- **Issue tracking**: GitHub Issues.

## What this architecture is not optimized for

It's worth naming the trade-offs:

- **Real-time data.** Monthly refresh is the design. Anyone needing live data should use the underlying agency tools.
- **Multi-county scaling.** The pipeline is Whatcom-tuned. Scaling to another county would require new source modules and re-tuning thresholds.
- **User-generated content.** No submission, no commenting, no annotation. By design.
- **Authentication.** Public read-only.
- **Mobile-first interaction.** Designed for tablet and desktop. Phone works but isn't the priority.
