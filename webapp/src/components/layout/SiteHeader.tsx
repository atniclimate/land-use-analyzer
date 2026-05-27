import { Link } from "@tanstack/react-router";

import { SITE, STORY_VIEWS } from "@/lib/site";
import { cn } from "@/lib/utils";

const linkClass =
  "rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring";

const activeClass = "text-primary font-semibold hover:text-primary";

export function SiteHeader() {
  return (
    <header className="border-b bg-card">
      <div className="container flex h-16 items-center justify-between gap-4">
        <Link to="/" className="flex items-center gap-2 font-semibold tracking-tight">
          <span className="inline-block h-3 w-3 rounded-sm bg-primary" aria-hidden="true" />
          <span>{SITE.name}</span>
        </Link>
        <nav aria-label="Story views" className="flex flex-wrap items-center gap-1">
          {STORY_VIEWS.map((view) => (
            <Link
              key={view.slug}
              to={view.path}
              className={linkClass}
              activeProps={{ className: cn(linkClass, activeClass) }}
            >
              {view.nav}
            </Link>
          ))}
          <Link
            to="/explore"
            className={linkClass}
            activeProps={{ className: cn(linkClass, activeClass) }}
          >
            Explore
          </Link>
          <Link
            to="/about"
            className={linkClass}
            activeProps={{ className: cn(linkClass, activeClass) }}
          >
            About
          </Link>
        </nav>
      </div>
    </header>
  );
}
