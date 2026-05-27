# Land Use Analyzer web app

Vite + React + TypeScript (strict). Renders the map, the four story views, an
explore mode, and a print/export view. Reads PMTiles from `public/tiles/` produced
by the Python pipeline. No backend.

This is the Phase 0 skeleton: the routes exist and render placeholder content with
the project palette and typography. Map rendering (MapLibre + deck.gl) and the data
layers land in Phase 1 (see `../PHASE_PLAN.md`).

## Prerequisites

- Node 20 or newer.
- pnpm (enable with `corepack enable pnpm`).

## Common commands

```powershell
# PowerShell - for the user to run
cd C:\dev\land-use-analyzer\webapp
pnpm install
pnpm dev        # http://localhost:5173
pnpm build      # type-check, bundle to dist/, copy 404.html
pnpm preview    # serve the production build locally
pnpm typecheck
pnpm lint
```

## Routes

| Path                   | View                                  |
| ---------------------- | ------------------------------------- |
| `/`                    | Landing, choose a story view          |
| `/flood`               | Flood story view                      |
| `/drought`             | Drought and changing seasons          |
| `/changing-hands`      | Sales velocity and ownership change   |
| `/building`            | Building activity (permits)           |
| `/explore`             | Layer-toggle exploration mode         |
| `/print/:view`         | Fixed-layout render target for PNG    |
| `/methodology/:topic`  | Methodology pages                     |
| `/about`               | About the project                     |

## Notes

- Strict TypeScript. No `any`. No `@ts-ignore` without a comment.
- All user-facing copy follows `../VOICE_GUIDE.md` (8th grade reading level).
- The production base path is `/land-use-analyzer/` for GitHub Pages; the router
  reads `import.meta.env.BASE_URL` to match.
