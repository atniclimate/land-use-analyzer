import { createRootRoute, createRoute, createRouter } from "@tanstack/react-router";

import { AboutPage } from "@/routes/about";
import { BuildingView } from "@/routes/building";
import { ChangingHandsView } from "@/routes/changing-hands";
import { DroughtView } from "@/routes/drought";
import { ExplorePage } from "@/routes/explore";
import { FloodView } from "@/routes/flood";
import { LandingPage } from "@/routes/index";
import { MethodologyPage } from "@/routes/methodology";
import { PrintView } from "@/routes/print";
import { RootLayout } from "@/routes/root";

const rootRoute = createRootRoute({ component: RootLayout });

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: LandingPage,
});

const floodRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/flood",
  component: FloodView,
});

const droughtRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/drought",
  component: DroughtView,
});

const changingHandsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/changing-hands",
  component: ChangingHandsView,
});

const buildingRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/building",
  component: BuildingView,
});

const exploreRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/explore",
  component: ExplorePage,
});

const printRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/print/$view",
  component: PrintView,
});

const methodologyRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/methodology/$topic",
  component: MethodologyPage,
});

const aboutRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/about",
  component: AboutPage,
});

const routeTree = rootRoute.addChildren([
  indexRoute,
  floodRoute,
  droughtRoute,
  changingHandsRoute,
  buildingRoute,
  exploreRoute,
  printRoute,
  methodologyRoute,
  aboutRoute,
]);

export const router = createRouter({
  routeTree,
  basepath: import.meta.env.BASE_URL,
  defaultPreload: "intent",
});

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
