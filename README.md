# Land Use Analyzer

A free, public tool that helps Whatcom County residents understand who owns the land around them, what environmental hazards their property faces, and how land is changing hands.

**Live demo**: https://atniclimate.github.io/land-use-analyzer/ (in development)

## What this is

Land Use Analyzer is a map. You can:

- See flood risk on any parcel in Whatcom County, based on FEMA, USGS, NOAA, and WA Department of Ecology data.
- See how the area has been affected by drought and changing seasons.
- See where land has been changing hands the fastest, and which areas are seeing the same buyer pick up multiple parcels.
- See where building permits have been pulled recently.
- Print or save any view as a PNG.

The data comes from public sources. We update it monthly.

## Who this is for

Anyone who lives in or cares about Whatcom County. We had farmers and rural residents in mind when we built it, but anyone can use it.

You don't need an account. We don't track you. We don't sell anything.

## How to use it

1. Open https://atniclimate.github.io/land-use-analyzer/ (demo URL).
2. Pick a story view, or explore the layers yourself.
3. Click any parcel for details.
4. Click "Export PNG" to save the current view.

## How it works

A Python pipeline pulls data from public sources, classifies parcels, and generates map tiles. A web app (built in TypeScript and React) renders the tiles in your browser. There is no backend. Your activity is not tracked.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details. See [DATA_SOURCES.md](./DATA_SOURCES.md) for the list of data sources. See [VOICE_GUIDE.md](./VOICE_GUIDE.md) if you're contributing copy.

## What this is not

- Not a real-time tool. We update monthly.
- Not legal or financial advice. The data is informational.
- Not a replacement for talking to your county assessor, treasurer, or local floodplain manager.
- Not affiliated with any political party or advocacy group.

## Contributing

We welcome contributions. A few things to know:

- This is a T0 baseline product for the general public in Whatcom County. Scope changes need discussion.
- Copy goes through [VOICE_GUIDE.md](./VOICE_GUIDE.md). Read it before writing user-facing text.
- New data sources go through [DATA_SOURCES.md](./DATA_SOURCES.md). Document the source, license, and refresh cadence.
- Code style: TypeScript strict mode, no `any`, no em dashes anywhere in the codebase.

Open an issue before starting work on anything substantial.

## Development

### Pipeline (Python)

```bash
cd pipeline
uv sync
./scripts/refresh.sh
```

This fetches all data sources and produces PMTiles in `webapp/public/tiles/`.

### Web app (TypeScript)

```bash
cd webapp
pnpm install
pnpm dev
```

Open http://localhost:5173.

### Building for deployment

```bash
cd webapp
pnpm build
```

Output is in `webapp/dist/`. Deploy to any static host.

## License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**. See [LICENSE.md](./LICENSE.md) for the full text.

In plain language: you can use this tool freely for personal study, research, education, public-interest work, and government work. You cannot use it commercially, fork it for your own product, or modify and redistribute it without explicit permission from the maintainer. If you want to do something the license does not cover, please open an issue.

## Credits

Built by community members in Whatcom County. Data from FEMA, USGS, NOAA, the Washington Department of Ecology, the US Drought Monitor, Whatcom County Assessor, and several other public agencies. Map tiles from CartoDB / OpenStreetMap.

## Data current as of

See the footer of the live site for the data date stamp.
