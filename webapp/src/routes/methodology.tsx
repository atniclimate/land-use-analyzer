import { useParams } from "@tanstack/react-router";

// Methodology pages explain how each layer is built and cite the agency sources.
// The full per-topic content lands alongside each layer in Phase 1.
export function MethodologyPage() {
  const { topic } = useParams({ from: "/methodology/$topic" });

  return (
    <div className="container py-8">
      <div className="max-w-2xl">
        <h1 className="text-2xl font-semibold tracking-tight">How we built this: {topic}</h1>
        <p className="mt-3 leading-relaxed text-muted-foreground">
          This page will explain where the data comes from, how we decide the Low, Medium, and High
          tiers, and what the data does and does not show. Sources are cited by name and link. The
          full methodology lands in Phase 1.
        </p>
      </div>
    </div>
  );
}
