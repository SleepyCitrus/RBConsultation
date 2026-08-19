import { readFile } from "fs/promises";
import path from "path";

export const SET_IDS = {
  ogn: "ogn", // Origins
  sfd: "sfd", // Spiritforged
  unl: "unl", // Unleashed
  ven: "ven", // Vendetta
} as const;

export type SetId = keyof typeof SET_IDS;

export type SetCatalog = {
  [key in SetId]: Card[];
};

export interface Card {
  id: string;
  name: string;
  riftbound_id: string;
  tcgplayer_id: string | null;
  collector_number: number;

  attributes: CardAttributes;

  classification: CardClassification;

  text: CardText;

  set: CardSet;

  media: CardMedia;

  orientation: "portrait" | "landscape" | string;

  metadata: CardMetadata;

  new: boolean;
}

export interface CardAttributes {
  energy: number | null;
  might: number | null;
  power: number | null;
}

export interface CardClassification {
  type: string;
  supertype: string;
  rarity: string;
  domain: string[];
}

export interface CardText {
  rich: string;
  plain: string;
  flavour: string | null;
}

export interface CardSet {
  set_id: string;
  label: string;
}

export interface CardMedia {
  image_url: string;
  artist: string;
  accessibility_text: string;
}

export interface CardMetadata {
  clean_name: string | null;
  updated_on: string; // ISO timestamp
  alternate_art: boolean;
  overnumbered: boolean;
  signature: boolean;
}

export async function loadAllCards(): Promise<SetCatalog> {
  const filePath = path.join(process.cwd(), "src/public/data/cards.json");
  const file = await readFile(filePath, "utf8");
  const setCatalog: SetCatalog = JSON.parse(file);
  return setCatalog;
}

export async function loadCards(setId: SetId, page: number = 1): Promise<Card[]> {
  if (setId in SET_IDS) {
    const filePath = path.join(process.cwd(), "src/public/data/cards.json");

    const file = await readFile(filePath, "utf8");

    const setCatalog: SetCatalog = JSON.parse(file);

    const cards: Card[] = setCatalog[setId];

    return cards.slice((page - 1) * 50, page * 50);
  }
  return [];
}
