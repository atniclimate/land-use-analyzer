import { SITE } from "@/lib/site";

export function AboutPage() {
  return (
    <div className="container py-8">
      <div className="max-w-2xl space-y-4">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">About this tool</h1>
        <p className="leading-relaxed text-muted-foreground">
          {SITE.name} is a free, public map of {SITE.county}, Washington. It helps you see who owns
          the land around you, what environmental hazards your property faces, and how land is
          changing hands over time.
        </p>
        <p className="leading-relaxed text-muted-foreground">
          The data comes from public agencies. We update it monthly. You do not need an account, and
          we do not track you.
        </p>
        <p className="leading-relaxed text-muted-foreground">
          Built by {SITE.attribution}. This is informational and is not legal or financial advice.
          It is not a replacement for talking to your county assessor, treasurer, or local
          floodplain manager.
        </p>
      </div>
    </div>
  );
}
