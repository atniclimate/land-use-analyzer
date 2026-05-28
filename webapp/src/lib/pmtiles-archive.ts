import { PMTiles } from "pmtiles";

// The parcel archive lives alongside the basemap and tile layers under /public/tiles/.
// HTTP range requests fetch only the tiles for the current viewport, so the full
// ~28 MB archive does not download up front.
export const parcelsArchive = new PMTiles(
  `${import.meta.env.BASE_URL}tiles/parcels.pmtiles`,
);
