export function ExplorePage() {
  return (
    <div className="container py-8">
      <div className="max-w-2xl">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Explore the layers</h1>
        <p className="mt-3 leading-relaxed text-muted-foreground">
          This mode lets you turn layers on and off and dig into the data yourself. You can adjust
          how the map flags large landholders, and view public-land and Tribal trust context layers.
          The layer controls land in Phase 1.
        </p>
      </div>

      <div
        role="img"
        aria-label="Map placeholder for explore mode of Whatcom County"
        className="mt-8 flex min-h-[28rem] items-center justify-center rounded-lg border border-dashed bg-muted/40 text-sm text-muted-foreground"
      >
        Map and layer controls go here in Phase 1
      </div>
    </div>
  );
}
