# Voice & Framing Guide

This guide tells anyone writing copy for **Land Use Analyzer** how to do it well. It applies to UI text, methodology pages, the README, error messages, tooltips, alt text, and any other words a visitor will read.

If you are writing copy for this project, **read this file first**. Every time.

---

## Who we're writing for

A 65-year-old dairy operator outside Sumas, who has heard the words "atmospheric river" too many times and wants to know if his fields are going to keep flooding.

A 34-year-old renter in Bellingham who reads the Cascadia Daily and wonders why her neighborhood feels different.

A 50-year-old berry grower near Lynden whose family has farmed since the 1920s and watched the parcel next door get bought by a name she doesn't recognize.

A retired teacher in Ferndale who clicks because the map looked interesting on Facebook.

A county planner double-checking a permit decision.

A high school student doing a project on local agriculture.

**Reading level: 8th grade.** Short sentences. Common words. Concrete examples.

## Three rules that override convenience

### 1. Name the hazard, not the politics

We describe what is on the land and what is happening to it. We do not tell people how to feel about it.

| Avoid | Prefer |
|-------|--------|
| "Vulnerable populations" | "Homes in the floodplain" |
| "Climate change impacts" | "More flooding, hotter summers, less snow" |
| "Corporate land grabs" | "Large companies buying farmland" |
| "Predatory acquisition" | "Several parcels bought by the same owner" |
| "At-risk communities" | "Areas that flood often" |

The reader can decide what to make of it.

### 2. Distinguish concentrated ownership from "anyone with an LLC"

A family LLC holding one homestead is not the story. A fund holding seventeen parcels through six shell companies is. Our classification thresholds enforce this in the data; **the copy has to match**.

| Avoid | Prefer |
|-------|--------|
| "Land owned by LLCs" | "Large landholdings owned by companies" |
| "Corporate ownership" (when describing tier highlights) | "Concentrated ownership" |
| "All LLCs are shown in black" | "Large landholders are shown in black. A family LLC holding one place is not highlighted here." |

### 3. Tenure is the divider, not category

A Canadian farming family in Lynden for three generations is not the same as a Canadian buyer who picked up a Birch Bay vacation home in 2018. The first is an established neighbor. The second is part of the recent acquisition pattern this map exists to surface. We separate them by **tenure**, not by where the mailing address points.

The map flags Foreign, Out-of-State, and Concentrated Corporate owners only when their current tenure on a parcel is **under 30 years**. Owners who have held the same parcel for 30+ years stay neutral, regardless of where their mailing address is.

This rule applies to all three flagged categories. It applies the same way. A Hong Kong shell company that bought a Lynden farm in 2024 and a retiree from Vancouver who bought a Point Roberts cabin in 2010 both light up. That is intentional. Whatcom County's housing affordability story includes second-home and vacation buying as much as it includes farmland consolidation. The map does not separate them because the underlying pattern (capital flowing into the county, pricing out residents with less of it) is shared.

| Avoid | Prefer |
|-------|--------|
| "Foreign buyers" (as a category) | "Out-of-country owners who bought in the past 30 years" |
| "Foreign-owned land" (as a standalone phrase) | Describe the pattern, e.g., "Out-of-country buyers have picked up 14 parcels in this area since 2010" |
| Highlighting any flagged category without naming tenure | Always name the tenure window when describing what's flagged |

If an established Canadian farming family is on the map, **we do not highlight them**. The 30-year rule does that work for us. The copy just reinforces what the data already shows.

## Tone

**Personable.** Like a neighbor explaining something over coffee, not a consultant presenting a slide deck.

**Community-oriented.** Words like "your area," "this corner of the county," "around here." Avoid "users," "stakeholders," "the public." We are talking to a person who lives here.

**Honest about uncertainty.** "Our best estimate," "this is what the data shows so far," "we update this monthly," "this layer comes from FEMA's mapping."

**Calm.** No alarm language. The data can speak for itself. If a parcel is in a high flood zone, we say it's in a high flood zone, not that it's "at imminent risk of catastrophe."

## Sentence structure

- Aim for **15 words per sentence on average**. Some shorter. Some a little longer.
- One idea per sentence.
- Active voice. "The county updates this map each month," not "This map is updated monthly by the county."
- Concrete nouns. "Flooding," not "hydrological events."
- Numbers in figures, not words: "3 sales in the past 2 years," not "three sales in the past two years."
- Spell out the first use of an acronym: "the Federal Emergency Management Agency (FEMA)."

## Sample story-view intros

These are templates. Adjust for accuracy, never for tone.

### Flood story view (~50 words, 8th grade)

> **Where the water goes**
>
> When the Nooksack rises, some parts of Whatcom County flood and some don't. This view shows where the highest flood risk is, based on federal flood maps and recent flood models. Red means a parcel is in the highest-risk area. Click any parcel to see its history.

### Drought & changing seasons (~50 words)

> **Hotter, drier, less snow**
>
> Whatcom County has gotten warmer over the past 50 years. Snowpack is melting earlier. Some summers are drier than they used to be. This view shows which areas have seen the biggest changes and which areas have been hit hardest by recent drought.

### Land changing hands (~60 words)

> **Who's buying around you**
>
> Some parcels stay in the same hands for generations. Others have changed hands recently. This view highlights parcels where the current owner has held the land for less than 30 years and lives outside Washington, outside the country, or is a company holding multiple parcels nearby. Long-established neighbors are not highlighted.

### Building activity nearby (~50 words)

> **What's being built nearby**
>
> Building permits tell you what's being constructed or changed on the land. This view shows where the most permits have been pulled in the past two years. It covers permits from the county and from each city in Whatcom County.

## Tooltips and on-hover text

Keep these to **one or two short sentences**.

- Good: "This parcel is in a FEMA high-risk flood zone. 12 acres."
- Bad: "This parcel has been designated by the Federal Emergency Management Agency as being within Zone AE, which represents the regulatory floodway and the 100-year flood event boundary."

## Legend text

- The legend is **not the place** to explain the methodology. Link to the methodology page.
- Use plain labels: "High flood risk," "Medium flood risk," "Low flood risk."
- Avoid jargon: not "Zone AE," not "1% AEP."

## Methodology page

This is where the technical detail goes. Still aim for clarity, but you can use more precise terms because the audience here has chosen to dig in.

- Cite sources by name and link.
- Explain thresholds explicitly: "We call a parcel 'high flood risk' if it falls within any of the following: ..."
- Acknowledge limits: "FEMA maps don't reflect every flood. Recent USGS modeling helps fill the gap, but no map is perfect."
- Date-stamp everything: "Data current as of [month, year]."

## Words to avoid

- "Stakeholder" → "neighbor," "resident," "owner," "person"
- "Leverage" → "use"
- "Robust" → "complete," "reliable"
- "Synergy" → just don't
- "Empower" → most uses are condescending; describe what the tool actually does
- "Disrupt" → say what's actually happening
- "Solution" → if it's a feature, call it a feature
- "Engagement" → in this project, this is plumbing word, not a goal
- "Vulnerable" (as a noun, "the vulnerable") → describe specifics

## Words that are fine

- "Your land," "your area," "your neighborhood"
- "We," "we update this monthly," "we use FEMA data"
- "Map," "see," "look," "click"
- "Owner," "landowner," "neighbor"
- "Farm," "field," "home," "lot"

## On capitalization

- **Indigenous, Tribal, Nations, Peoples, Knowledge** are capitalized when used. (Rare in this T0 product, but if Tribal trust land appears in any UI copy, this rule holds.)
- **FEMA, NOAA, USGS, USDA, WA Department of Ecology** are spelled out on first use.
- "Whatcom County" is two words, both capitalized.
- City names are capitalized: Bellingham, Lynden, Ferndale, Blaine, Sumas, Everson, Nooksack, Birch Bay (technically unincorporated).

## On punctuation

- **No em dashes.** Use commas, parens, or a separate sentence.
- Oxford comma: yes.
- Sentence-case headings, not Title Case.
- One space after a period.
- Hyphenate "out-of-state," "out-of-country," "8th-grade reading level."

## Accessibility

- Color is never the only way information is conveyed. Patterns, icons, or text labels accompany every color cue.
- Minimum contrast ratio is **4.5:1** for body text against background.
- Every interactive element has a focus state.
- Alt text on map screenshots describes the data shown, not just "map of Whatcom County."

## When in doubt

Read the sentence aloud. If you wouldn't say it to a neighbor over coffee, rewrite it.

If you have to use a technical term, define it on first use, then use it.

If you're tempted to add a hedge like "potentially," "possibly," or "may," ask whether the data actually supports the claim. If yes, drop the hedge. If no, drop the claim.
