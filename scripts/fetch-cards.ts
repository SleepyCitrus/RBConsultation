import { Card, SET_IDS } from "@/src/lib/card-loader";
import { writeFile } from "fs/promises";

const API_URL = "https://api.riftcodex.com/cards";

function sortCards(cards: Card[]) {
  return cards.sort((a, b) => {
    // Then sort by riftbound_id
    return a.riftbound_id.localeCompare(b.riftbound_id);
  });
}

interface GetCardsResponse {
  items: Card[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

interface CardData {
  id: string;
  [key: string]: any;
}

function isObject(item: any): boolean {
  return item && typeof item === "object" && !Array.isArray(item);
}

function deepMerge(target: any, source: any): any {
  const output = { ...target };

  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach((key) => {
      const sourceValue = source[key];
      const targetValue = target[key];

      // If source value is null or undefined, keep the target's value
      if (sourceValue === null || sourceValue === undefined) {
        return;
      }

      if (isObject(sourceValue)) {
        if (!(key in target) || targetValue === null) {
          output[key] = sourceValue;
        } else {
          output[key] = deepMerge(targetValue, sourceValue);
        }
      } else {
        output[key] = sourceValue;
      }
    });
  }
  return output;
}

type CardLookupKeys = {
  [K in keyof Card]: Card[K] extends string | number ? K : never;
}[keyof Card]; // Results in: "id" | "name" | "riftbound_id" | "collector_number"

function mergeDuplicateCards(items: Card[], uniqueKey: CardLookupKeys): Card[] {
  // Now TypeScript knows keyValue can ONLY be a string or a number
  const mergedMap = new Map<string | number, Card>();

  items.forEach((item) => {
    const keyValue = item[uniqueKey];

    if (keyValue === null || keyValue === undefined) return;

    if (mergedMap.has(keyValue)) {
      const existingItem = mergedMap.get(keyValue)!;
      mergedMap.set(keyValue, deepMerge(existingItem, item));
    } else {
      mergedMap.set(keyValue, item);
    }
  });

  return Array.from(mergedMap.values());
}

async function fetchAllCards(setId: string): Promise<Card[]> {
  const allCards: Card[] = [];

  let page = 1;
  let hasMore = true;
  let totalCards = 0;

  while (hasMore) {
    const params = new URLSearchParams({
      sort: "collector_number",
      set_id: setId,
      dir: "1",
      page: page.toString(),
      size: "100",
    });

    const response = await fetch(`${API_URL}?${params.toString()}`);

    if (!response.ok) {
      throw new Error(`API failed: ${response.status}`);
    }

    const data: GetCardsResponse = await response.json();

    const mergedCards = mergeDuplicateCards(data.items, "riftbound_id");
    allCards.push(...mergedCards);

    totalCards = data.total;

    if (page < data.pages) {
      page++;
    } else {
      hasMore = false;
    }
  }

  console.log(`Found ${totalCards} cards for set ${setId}...`);
  console.log(`Merged down to ${allCards.length} cards for set ${setId}...`);

  return allCards;
}

async function main() {
  const cardList: { [key: string]: Card[] } = {};

  for (const [_, setId] of Object.entries(SET_IDS)) {
    const cards = await fetchAllCards(setId);
    const sortedCards = sortCards(cards);

    cardList[setId] = sortedCards;
  }

  await writeFile("src/public/data/cards.json", JSON.stringify(cardList, null, 2));

  console.log(`Saved ${Object.keys(cardList).join(", ")} cards.`);
}

main();
