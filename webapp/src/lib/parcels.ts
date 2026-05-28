import { z } from "zod";

// Mirrors lus_pipeline.classify.OwnershipCategory. Keep in sync with the pipeline.
export const OWNERSHIP_CATEGORIES = [
  "government_tribal_utility",
  "concentrated_corporate",
  "small_corporate",
  "out_of_state",
  "foreign",
  "local",
] as const;

export const ownershipCategorySchema = z.enum(OWNERSHIP_CATEGORIES);
export type OwnershipCategory = z.infer<typeof ownershipCategorySchema>;

export const MAILING_SIGNALS = ["wa", "out_of_state", "foreign", "unknown"] as const;
export const mailingSignalSchema = z.enum(MAILING_SIGNALS);
export type MailingSignal = z.infer<typeof mailingSignalSchema>;

export const parcelPropertiesSchema = z.object({
  prop_id: z.string(),
  owner: z.string(),
  mailing_state: z.string(),
  mailing_country: z.string(),
  acres: z.number().nullable(),
  assessed_value: z.number().nullable(),
  ownership_category: ownershipCategorySchema,
  mailing_signal: mailingSignalSchema,
  tenure_years: z.number().nullable(),
  flagged: z.boolean(),
});
export type ParcelProperties = z.infer<typeof parcelPropertiesSchema>;

// Validate only the envelope here. Validating all ~118k features with Zod is too
// slow; useParcels spot-checks one feature's properties to catch schema drift.
export const featureCollectionEnvelopeSchema = z.object({
  type: z.literal("FeatureCollection"),
  features: z.array(z.unknown()),
});

export const parcelsMetaSchema = z.object({
  tenure_source: z.string(),
  parcel_count: z.number(),
  generated: z.string(),
});
export type ParcelsMeta = z.infer<typeof parcelsMetaSchema>;

export type Rgba = [number, number, number, number];

export interface CategoryStyle {
  label: string;
  color: Rgba;
}

// Palette derived from Okabe-Ito: colorblind-safe, no red/green confusion, equal
// luminance across the flagged categories so none dominates by brightness alone.
// Concentrated Corporate is violet, not black: black reads as "redlined" and
// overstates the story in dense urban areas. Color is never the only cue: the
// legend pairs every color with a label that names the tenure window where it
// applies (see VOICE_GUIDE.md).
export const CATEGORY_STYLE: Record<OwnershipCategory, CategoryStyle> = {
  concentrated_corporate: { label: "Large landholder (concentrated)", color: [122, 79, 176, 200] },
  out_of_state: { label: "Out-of-state owner, bought recently", color: [0, 114, 178, 195] },
  foreign: { label: "Out-of-country owner, bought recently", color: [204, 121, 167, 195] },
  small_corporate: { label: "Company or LLC (small)", color: [189, 182, 168, 110] },
  government_tribal_utility: { label: "Government, Tribal, or utility", color: [94, 140, 106, 110] },
  local: { label: "Local or long-established", color: [242, 239, 233, 50] },
};

// Muted background tints for parcels classified as LOCAL whose RAW mailing signal
// is out-of-state or out-of-country. Refines rule #2 from a binary to a gradient:
// established neighbors stay quiet but the underlying mailing pattern is visible.
export interface MailingMutedStyle {
  label: string;
  color: Rgba;
}
export const MAILING_MUTED_STYLE: Record<"out_of_state" | "foreign", MailingMutedStyle> = {
  out_of_state: { label: "Out-of-state owner, long-established", color: [169, 199, 222, 135] },
  foreign: { label: "Out-of-country owner, long-established", color: [226, 196, 210, 135] },
};
