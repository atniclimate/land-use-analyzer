import { Link } from "@tanstack/react-router";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SITE, STORY_VIEWS } from "@/lib/site";

export function LandingPage() {
  return (
    <div className="container py-10">
      <section className="max-w-2xl">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{SITE.name}</h1>
        <p className="mt-4 text-lg leading-relaxed text-muted-foreground">{SITE.description}</p>
        <p className="mt-2 text-sm text-muted-foreground">
          Pick a view to start, or explore the layers yourself.
        </p>
      </section>

      <section className="mt-10 grid gap-6 sm:grid-cols-2">
        {STORY_VIEWS.map((view) => (
          <Link
            key={view.slug}
            to={view.path}
            className="group rounded-lg focus-visible:outline-none"
          >
            <Card className="h-full transition-colors group-hover:border-primary group-focus-visible:ring-2 group-focus-visible:ring-ring">
              <CardHeader>
                <CardTitle>{view.title}</CardTitle>
                <CardDescription>{view.nav}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed text-muted-foreground">{view.intro}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </section>

      <section className="mt-6">
        <Link to="/explore" className="group block rounded-lg focus-visible:outline-none">
          <Card className="h-full transition-colors group-hover:border-primary group-focus-visible:ring-2 group-focus-visible:ring-ring">
            <CardHeader>
              <CardTitle>Explore the layers</CardTitle>
              <CardDescription>Or browse on your own</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed text-muted-foreground">
                All four maps on one page. Toggle the layers you want to see. Click any parcel for
                owner, acres, value, and tenure.
              </p>
            </CardContent>
          </Card>
        </Link>
      </section>
    </div>
  );
}
