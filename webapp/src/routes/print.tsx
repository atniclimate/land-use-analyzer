import { useParams } from "@tanstack/react-router";

// Fixed-layout render target for PNG export. The real export composition (map,
// legend, title, scale bar, north arrow, attribution, date) lands in Phase 1g.
export function PrintView() {
  const { view } = useParams({ from: "/print/$view" });

  return (
    <div className="container py-8">
      <h1 className="text-xl font-semibold tracking-tight">Print view: {view}</h1>
      <div
        role="img"
        aria-label={`Print layout placeholder for the ${view} view`}
        className="mt-4 flex aspect-[16/10] items-center justify-center rounded-lg border border-dashed bg-muted/40 text-sm text-muted-foreground"
      >
        Export layout goes here in Phase 1
      </div>
    </div>
  );
}
