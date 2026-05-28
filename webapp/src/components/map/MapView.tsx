import { useEffect, useRef } from "react";

import maplibregl from "maplibre-gl";

import { cn } from "@/lib/utils";

import "maplibre-gl/dist/maplibre-gl.css";

// Keyless CARTO Positron vector style. Calm light basemap that suits the palette.
const CARTO_POSITRON_STYLE = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json";

// Whatcom County, WA.
const WHATCOM_CENTER: [number, number] = [-122.35, 48.78];
const DEFAULT_ZOOM = 9;

interface MapViewProps {
  ariaLabel: string;
  className?: string;
  onReady?: (map: maplibregl.Map) => void;
}

export function MapView({ ariaLabel, className, onReady }: MapViewProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const onReadyRef = useRef(onReady);
  onReadyRef.current = onReady;

  useEffect(() => {
    const container = containerRef.current;
    if (!container || mapRef.current) {
      return;
    }

    const map = new maplibregl.Map({
      container,
      style: CARTO_POSITRON_STYLE,
      center: WHATCOM_CENTER,
      zoom: DEFAULT_ZOOM,
      attributionControl: false,
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    map.addControl(
      new maplibregl.AttributionControl({
        compact: true,
        customAttribution: "© OpenStreetMap contributors © CARTO",
      }),
      "bottom-right",
    );

    mapRef.current = map;
    map.on("load", () => onReadyRef.current?.(map));

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  return (
    <div
      ref={containerRef}
      role="region"
      aria-label={ariaLabel}
      className={cn("h-full w-full", className)}
    />
  );
}
