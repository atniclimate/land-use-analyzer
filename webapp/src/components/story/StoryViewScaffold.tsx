import { Link } from "@tanstack/react-router";

import { ParcelMap } from "@/components/map/ParcelMap";
import { buttonVariants } from "@/components/ui/button";
import { type StoryView } from "@/lib/site";

interface StoryViewScaffoldProps {
  view: StoryView;
}

// Phase 1a status: only ownership data exists. Each story view shows its title and
// intro, then the shared parcel map. Story-specific layers (flood / drought /
// building) land in their own phases; until then the parcels still read as the
// background context for those views.
export function StoryViewScaffold({ view }: StoryViewScaffoldProps) {
  const isOwnershipStory = view.slug === "changing-hands";

  return (
    <div className="container py-8">
      <div className="max-w-2xl">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{view.title}</h1>
        <p className="mt-3 leading-relaxed text-muted-foreground">{view.intro}</p>
        <p className="mt-3 text-sm text-muted-foreground">
          {isOwnershipStory
            ? "Parcels are colored by who owns them. Long-established neighbors stay neutral. Click any parcel for owner, acres, value, and how long they have held it."
            : `${view.nav} data lands in a later phase. For now the map shows parcels colored by who owns them, like on the Explore page.`}
        </p>
        <div className="mt-4">
          <Link
            to="/methodology/$topic"
            params={{ topic: view.slug }}
            className={buttonVariants({ variant: "outline", size: "sm" })}
          >
            How we built this
          </Link>
        </div>
      </div>

      <div className="mt-8 h-[32rem] overflow-hidden rounded-lg border">
        <ParcelMap ariaLabel={`Map of Whatcom County for the ${view.nav} story view`} />
      </div>
    </div>
  );
}
