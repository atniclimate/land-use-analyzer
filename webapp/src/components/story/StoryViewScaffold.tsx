import { Link } from "@tanstack/react-router";

import { MapView } from "@/components/map/MapView";
import { buttonVariants } from "@/components/ui/button";
import { TIERS, type StoryView } from "@/lib/site";

interface StoryViewScaffoldProps {
  view: StoryView;
}

// Placeholder layout for a story view. The map (MapLibre + deck.gl) and the real
// legend land in Phase 1; this fixes the page shape, copy slot, and legend slot.
export function StoryViewScaffold({ view }: StoryViewScaffoldProps) {
  return (
    <div className="container py-8">
      <div className="max-w-2xl">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{view.title}</h1>
        <p className="mt-3 leading-relaxed text-muted-foreground">{view.intro}</p>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_18rem]">
        <div className="h-[32rem] overflow-hidden rounded-lg border">
          <MapView ariaLabel={`Map of Whatcom County for the ${view.nav} story view`} />
        </div>

        <aside className="space-y-4">
          <div className="rounded-lg border bg-card p-4">
            <h2 className="text-sm font-semibold">Legend</h2>
            <ul className="mt-3 space-y-2">
              {TIERS.map((tier) => (
                <li key={tier.key} className="flex items-center gap-2 text-sm">
                  <span
                    className="inline-block h-3 w-3 rounded-sm border"
                    style={{ backgroundColor: `hsl(var(${tier.varName}))` }}
                    aria-hidden="true"
                  />
                  <span>{tier.label} risk</span>
                </li>
              ))}
            </ul>
          </div>
          <Link
            to="/methodology/$topic"
            params={{ topic: view.slug }}
            className={buttonVariants({ variant: "outline", size: "sm" })}
          >
            How we built this
          </Link>
        </aside>
      </div>
    </div>
  );
}
