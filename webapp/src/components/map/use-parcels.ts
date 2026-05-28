import { useEffect, useState } from "react";

import { parcelsMetaSchema, type ParcelsMeta } from "@/lib/parcels";

export type ParcelStatus = "loading" | "ready" | "error";

export interface ParcelMetaState {
  status: ParcelStatus;
  meta: ParcelsMeta | null;
}

// The parcel features themselves stream from PMTiles via deck.gl's TileLayer (see
// pmtiles-archive.ts and ParcelMap.tsx). This hook only fetches the small meta
// sidecar so the UI can mark tenure as "data needed" when it is placeholder.
export function useParcelsMeta(): ParcelMetaState {
  const [state, setState] = useState<ParcelMetaState>({ status: "loading", meta: null });

  useEffect(() => {
    let cancelled = false;
    const base = import.meta.env.BASE_URL;

    async function load() {
      try {
        const resp = await fetch(`${base}tiles/parcels.meta.json`);
        if (!resp.ok) {
          throw new Error(`parcels.meta.json: ${resp.status}`);
        }
        const meta = parcelsMetaSchema.parse(await resp.json());
        if (!cancelled) {
          setState({ status: "ready", meta });
        }
      } catch (error) {
        if (!cancelled) {
          console.error("Failed to load parcels meta:", error);
          setState({ status: "error", meta: null });
        }
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}
