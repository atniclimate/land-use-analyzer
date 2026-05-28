import { ParcelMap } from "@/components/map/ParcelMap";

export function ExplorePage() {
  return (
    <div className="container py-8">
      <div className="max-w-2xl">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Explore the layers</h1>
        <p className="mt-3 leading-relaxed text-muted-foreground">
          Every parcel in Whatcom County is on this map, colored by who owns it. Click any parcel to
          see the owner, acres, value, and how long they have held it. Long-established neighbors
          stay neutral. More layers and controls land in later phases.
        </p>
      </div>

      <div className="mt-8 h-[70vh] overflow-hidden rounded-lg border">
        <ParcelMap ariaLabel="Interactive map of Whatcom County parcels" />
      </div>
    </div>
  );
}
