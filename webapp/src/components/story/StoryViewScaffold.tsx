import { Link } from "@tanstack/react-router";

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
        <div
          role="img"
          aria-label={`Map placeholder for the ${view.nav} story view of Whatcom County`}
          className="flex min-h-[24rem] items-center justify-center rounded-lg border border-dashed bg-muted/40 text-sm text-muted-foreground"
        >
          Map goes here in Phase 1
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
