// Static site metadata and story-view configuration. UI copy follows VOICE_GUIDE.md
// (8th grade reading level, environmental-hazard framing, no em dashes).

export const SITE = {
  name: "Land Use Analyzer",
  description:
    "See who owns the land around you in Whatcom County, what environmental hazards your property faces, and how land is changing hands.",
  county: "Whatcom County",
  attribution: "ATNI Climate",
  repoUrl: "https://github.com/atniclimate/land-use-analyzer",
} as const;

export type StoryPath = "/flood" | "/drought" | "/changing-hands" | "/building";

export interface StoryView {
  slug: string;
  path: StoryPath;
  nav: string;
  title: string;
  intro: string;
}

export const STORY_VIEWS: StoryView[] = [
  {
    slug: "flood",
    path: "/flood",
    nav: "Flood",
    title: "Where the water goes",
    intro:
      "When the Nooksack rises, some parts of Whatcom County flood and some do not. This view shows where the highest flood risk is, based on federal flood maps and recent flood models. Click any parcel to see its history.",
  },
  {
    slug: "drought",
    path: "/drought",
    nav: "Drought",
    title: "Hotter, drier, less snow",
    intro:
      "Whatcom County has gotten warmer over the past 50 years. Snowpack is melting earlier. Some summers are drier than they used to be. This view shows which areas have changed the most and which have been hit hardest by recent drought.",
  },
  {
    slug: "changing-hands",
    path: "/changing-hands",
    nav: "Changing hands",
    title: "Who's buying around you",
    intro:
      "Some parcels stay in the same hands for generations. This view highlights parcels where the current owner has held the land for less than 30 years and lives out of state, out of the country, or is a company holding several parcels nearby. Long-established neighbors are not highlighted.",
  },
  {
    slug: "building",
    path: "/building",
    nav: "Building",
    title: "What's being built nearby",
    intro:
      "Building permits tell you what is being constructed or changed on the land. This view shows where the most permits have been pulled in the past 2 years. It covers permits from the county and from each city in Whatcom County.",
  },
];

export function getStoryView(slug: string): StoryView {
  const view = STORY_VIEWS.find((v) => v.slug === slug);
  if (!view) {
    throw new Error(`Unknown story view: ${slug}`);
  }
  return view;
}

export const TIERS = [
  { key: "low", label: "Low", varName: "--tier-low" },
  { key: "medium", label: "Medium", varName: "--tier-medium" },
  { key: "high", label: "High", varName: "--tier-high" },
] as const;
