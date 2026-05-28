import { useCallback, useEffect, useRef, useState } from "react";

import { TileLayer } from "@deck.gl/geo-layers";
import { GeoJsonLayer } from "@deck.gl/layers";
import { MapboxOverlay } from "@deck.gl/mapbox";
import { load } from "@loaders.gl/core";
import { MVTLoader } from "@loaders.gl/mvt";
import { Link } from "@tanstack/react-router";
import type { Feature, Geometry } from "geojson";
import type { Map as MapLibreMap } from "maplibre-gl";

import {
  CATEGORY_STYLE,
  MAILING_MUTED_STYLE,
  type OwnershipCategory,
  type ParcelProperties,
  type Rgba,
} from "@/lib/parcels";
import { parcelsArchive } from "@/lib/pmtiles-archive";

import { MapView } from "./MapView";
import { useParcelsMeta } from "./use-parcels";

type ParcelFeature = Feature<Geometry, ParcelProperties>;

const NEUTRAL_FILL: Rgba = CATEGORY_STYLE.local.color;
const LINE_COLOR: Rgba = [80, 80, 80, 90];

const LEGEND_ITEMS: { color: Rgba; label: string }[] = [
  { color: CATEGORY_STYLE.concentrated_corporate.color, label: CATEGORY_STYLE.concentrated_corporate.label },
  { color: CATEGORY_STYLE.out_of_state.color, label: CATEGORY_STYLE.out_of_state.label },
  { color: CATEGORY_STYLE.foreign.color, label: CATEGORY_STYLE.foreign.label },
  { color: MAILING_MUTED_STYLE.out_of_state.color, label: MAILING_MUTED_STYLE.out_of_state.label },
  { color: MAILING_MUTED_STYLE.foreign.color, label: MAILING_MUTED_STYLE.foreign.label },
  { color: CATEGORY_STYLE.small_corporate.color, label: CATEGORY_STYLE.small_corporate.label },
  { color: CATEGORY_STYLE.government_tribal_utility.color, label: CATEGORY_STYLE.government_tribal_utility.label },
  { color: CATEGORY_STYLE.local.color, label: CATEGORY_STYLE.local.label },
];

const usd = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function formatAcres(acres: number | null): string {
  if (acres == null) return "unknown";
  if (acres > 0 && acres < 0.01) return "less than 0.01";
  return acres.toFixed(2);
}

function formatAssessedValue(value: number | null, category: OwnershipCategory): string {
  if (value == null) return "unknown";
  if (value === 0) {
    return category === "government_tribal_utility" ? "Exempt" : "No assessment on file";
  }
  return usd.format(value);
}

function fillColor(feature: { properties: ParcelProperties }): Rgba {
  const props = feature.properties;
  if (props.ownership_category === "local") {
    if (props.mailing_signal === "out_of_state") return MAILING_MUTED_STYLE.out_of_state.color;
    if (props.mailing_signal === "foreign") return MAILING_MUTED_STYLE.foreign.color;
  }
  return CATEGORY_STYLE[props.ownership_category as OwnershipCategory]?.color ?? NEUTRAL_FILL;
}

function buildParcelTileLayer(onSelect: (p: ParcelProperties) => void): TileLayer<ParcelFeature[]> {
  return new TileLayer<ParcelFeature[]>({
    id: "parcels-tiles",
    minZoom: 8,
    maxZoom: 14,
    tileSize: 512,
    pickable: true,
    onClick: (info) => {
      const feature = info.object as ParcelFeature | undefined;
      if (feature?.properties) {
        onSelect(feature.properties);
      }
    },
    getTileData: async ({ index, signal }) => {
      const { x, y, z } = index;
      const tile = await parcelsArchive.getZxy(z, x, y, signal ?? undefined);
      if (!tile) {
        return [];
      }
      const features = (await load(tile.data, MVTLoader, {
        mvt: {
          coordinates: "wgs84",
          layers: ["parcels"],
          tileIndex: { x, y, z },
        },
      })) as ParcelFeature[];
      return features;
    },
    renderSubLayers: (props) => {
      const data = (props.data ?? []) as ParcelFeature[];
      return new GeoJsonLayer<ParcelProperties>({
        id: `${props.id}-poly`,
        data,
        filled: true,
        stroked: true,
        getFillColor: fillColor,
        getLineColor: LINE_COLOR,
        getLineWidth: 0,
        lineWidthMinPixels: 0.4,
        pickable: true,
        autoHighlight: true,
        highlightColor: [255, 255, 255, 120],
      });
    },
  });
}

export function ParcelMap({ ariaLabel }: { ariaLabel: string }) {
  const { status, meta } = useParcelsMeta();
  const overlayRef = useRef<MapboxOverlay | null>(null);
  const [selected, setSelected] = useState<ParcelProperties | null>(null);

  const installLayers = useCallback(() => {
    if (overlayRef.current) {
      overlayRef.current.setProps({ layers: [buildParcelTileLayer(setSelected)] });
    }
  }, []);

  const handleReady = useCallback(
    (map: MapLibreMap) => {
      const overlay = new MapboxOverlay({ interleaved: true, layers: [] });
      map.addControl(overlay);
      overlayRef.current = overlay;
      installLayers();
    },
    [installLayers],
  );

  // Layers are bound to the PMTiles archive (stable), so we only need to install
  // them once when the map is ready. No effect on meta updates needed.
  useEffect(() => {
    installLayers();
  }, [installLayers]);

  const tenurePlaceholder = meta?.tenure_source === "placeholder";

  return (
    <div className="relative h-full w-full">
      <MapView ariaLabel={ariaLabel} onReady={handleReady} />

      <DataSources tenurePlaceholder={tenurePlaceholder} />
      <Legend />

      {status === "loading" && <StatusBadge text="Loading parcels..." />}
      {status === "error" && (
        <StatusBadge text="Could not load parcel metadata. Run the pipeline to generate the tiles." />
      )}

      {selected && (
        <ParcelDetail
          parcel={selected}
          tenurePlaceholder={tenurePlaceholder}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}

function StatusBadge({ text }: { text: string }) {
  return (
    <div className="absolute inset-x-0 top-1/2 mx-auto w-fit -translate-y-1/2 rounded-md bg-card/95 px-4 py-2 text-sm text-muted-foreground shadow">
      {text}
    </div>
  );
}

function DataSources({ tenurePlaceholder }: { tenurePlaceholder: boolean }) {
  return (
    <div className="absolute left-3 top-3 max-w-xs rounded-md border bg-card/95 p-3 text-xs shadow">
      <h2 className="mb-2 font-semibold">Data sources</h2>
      <ul className="space-y-2">
        <li className="flex items-start gap-2">
          <span
            className="mt-1 inline-block h-2 w-2 shrink-0 rounded-full bg-emerald-500"
            aria-hidden="true"
          />
          <div>
            <div className="font-medium text-foreground">Owner and mailing</div>
            <div className="text-muted-foreground">Whatcom County Assessor, 2026-05-01</div>
          </div>
        </li>
        <li className="flex items-start gap-2">
          <span
            className={`mt-1 inline-block h-2 w-2 shrink-0 rounded-full ${tenurePlaceholder ? "bg-amber-500" : "bg-emerald-500"}`}
            aria-hidden="true"
          />
          {tenurePlaceholder ? (
            <Link
              to="/methodology/$topic"
              params={{ topic: "tenure" }}
              className="block rounded-sm hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <span className="flex flex-wrap items-center gap-x-2 font-medium text-foreground">
                <span>Tenure (years held)</span>
                <span className="rounded bg-amber-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-amber-900">
                  Data needed
                </span>
              </span>
              <span className="block text-muted-foreground">
                Placeholder shown. Real sale dates not yet sourced.
              </span>
            </Link>
          ) : (
            <div>
              <div className="flex flex-wrap items-center gap-x-2 font-medium text-foreground">
                <span>Tenure (years held)</span>
              </div>
              <div className="text-muted-foreground">Sale dates from the assessor.</div>
            </div>
          )}
        </li>
      </ul>
    </div>
  );
}

function Legend() {
  return (
    <div className="absolute bottom-3 left-3 max-w-xs rounded-md border bg-card/95 p-3 text-xs shadow">
      <h2 className="mb-2 font-semibold">Who owns it</h2>
      <ul className="space-y-1.5">
        {LEGEND_ITEMS.map((item) => {
          const [r, g, b, a] = item.color;
          return (
            <li key={item.label} className="flex items-center gap-2">
              <span
                className="inline-block h-3 w-3 shrink-0 rounded-sm border border-black/15"
                style={{ backgroundColor: `rgba(${r}, ${g}, ${b}, ${a / 255})` }}
                aria-hidden="true"
              />
              <span>{item.label}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

function ParcelDetail({
  parcel,
  tenurePlaceholder,
  onClose,
}: {
  parcel: ParcelProperties;
  tenurePlaceholder: boolean;
  onClose: () => void;
}) {
  const location = parcel.mailing_country
    ? `Owner mails from ${parcel.mailing_country}`
    : parcel.mailing_state
      ? `Owner mails from ${parcel.mailing_state}`
      : "Owner mailing address unknown";

  const categoryLabel =
    parcel.ownership_category === "local" && parcel.mailing_signal === "out_of_state"
      ? MAILING_MUTED_STYLE.out_of_state.label
      : parcel.ownership_category === "local" && parcel.mailing_signal === "foreign"
        ? MAILING_MUTED_STYLE.foreign.label
        : CATEGORY_STYLE[parcel.ownership_category].label;

  return (
    <div className="absolute right-3 top-3 w-72 rounded-md border bg-card/95 p-4 text-sm shadow-lg">
      <div className="flex items-start justify-between gap-2">
        <h2 className="font-semibold leading-tight">{parcel.owner || "Unknown owner"}</h2>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close parcel details"
          className="rounded px-1 text-muted-foreground hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          ×
        </button>
      </div>
      <dl className="mt-3 space-y-1.5 text-muted-foreground">
        <Row label="Category" value={categoryLabel} />
        <Row label="Where" value={location} />
        <Row label="Acres" value={formatAcres(parcel.acres)} />
        <Row
          label="Assessed value"
          value={formatAssessedValue(parcel.assessed_value, parcel.ownership_category)}
        />
        <Row
          label="Years held"
          value={parcel.tenure_years != null ? `${parcel.tenure_years}` : "unknown"}
        />
      </dl>
      {tenurePlaceholder && (
        <p className="mt-3 text-xs text-amber-700">Years held is placeholder demo data.</p>
      )}
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-3">
      <dt>{label}</dt>
      <dd className="text-right font-medium text-foreground">{value}</dd>
    </div>
  );
}
