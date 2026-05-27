import { SITE } from "@/lib/site";

export function SiteFooter() {
  return (
    <footer className="border-t bg-card">
      <div className="container flex flex-col gap-3 py-8 text-sm text-muted-foreground">
        <p>
          Built by {SITE.attribution}. Data from public agencies including FEMA, USGS, NOAA, the
          Washington Department of Ecology, the US Drought Monitor, and the Whatcom County Assessor.
        </p>
        <p>No accounts. No tracking. No cookies. We update the data monthly.</p>
        <p>
          Data current as of <span className="font-medium text-foreground">a date shown here</span>.
          This tool is informational and is not legal or financial advice.
        </p>
        <p>
          Licensed under PolyForm Noncommercial 1.0.0.{" "}
          <a
            href={SITE.repoUrl}
            className="font-medium text-foreground underline underline-offset-4 hover:text-primary"
          >
            Source on GitHub
          </a>
          .
        </p>
      </div>
    </footer>
  );
}
