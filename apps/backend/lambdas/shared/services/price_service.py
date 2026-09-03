import logging
import os
import time
from typing import Optional

import requests
from ingestion.justtcg.justtcg_card import JustTCGCard
from shared.logging.logger import logger
from shared.riftbound.riftbound_booster_pack import FOIL, NEAR_MINT, NORMAL, SEALED
from shared.riftbound.riftbound_metadata import COMMON, RIFTBOUND, UNCOMMON
from shared.riftcodex.riftcodex_item import RiftcodexItem
from shared.services.catalog_service import CatalogService

GAMES_URL = "https://api.justtcg.com/v1/games"
CARDS_URL = "https://api.justtcg.com/v1/cards"


@logger
class PriceService:
    logger: logging.Logger

    def __init__(self, catalogService: CatalogService):
        self.catalogService = catalogService

    def get_game_slugs(self):
        response = requests.get(
            GAMES_URL, headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]}
        )

        response.raise_for_status()

        for game in response.json()["data"]:
            if game["id"].contains("riftbound"):
                self.logger.info(f"Found game: {game['id']} - {game['name']}")
                return game["id"]

    def get_price(self, tcgplayerId: str, duration: str = "7d") -> JustTCGCard:
        """
        Gets the price history of a single card.
        If getting multiple cards, use get_prices() instead.
        """

        params = {
            "game": RIFTBOUND,
            "tcgplayerId": "652814",
            "condition": SEALED,
            "language": "English",
        }

        return self.get_with_retry(params=params, chunk=None)[0]

    def get_with_retry(
        self, params: Optional[dict], chunk: Optional[list[dict]]
    ) -> list[JustTCGCard]:
        results: list[JustTCGCard] = []

        for attempt in range(5):
            response: requests.Response

            if params:
                # singular request, use get instead of post
                response = requests.get(
                    CARDS_URL,
                    headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]},
                    params=params,
                )
            elif chunk:
                response = requests.post(
                    CARDS_URL,
                    headers={
                        "x-api-key": os.environ["JUSTTCG_API_KEY"],
                        "Content-Type": "application/json",
                    },
                    json=chunk,
                )
            else:
                return []

            if response.status_code != 429:
                # Not a throttling issue, either raise error or return results
                response.raise_for_status()
                if response.json():
                    if response.json()["data"]:
                        for card in response.json()["data"]:
                            justtcg_card = JustTCGCard.model_validate(card)
                            results.append(justtcg_card)

                return results

            retry_after = response.headers.get("Retry-After")

            if retry_after:
                wait = float(retry_after)
            else:
                # Free tier limits is 10 requests / min so worst case wait 60 seconds before retrying.
                wait = 60

            self.logger.info(
                f"Throttled by JustTCG API. Retrying in {wait} seconds: {response}"
            )
            time.sleep(wait)

        return results

    def get_prices(
        self, cards: dict[str, RiftcodexItem], duration: str = "7d"
    ) -> list[JustTCGCard]:
        card_requests = []
        for tcgplayer_id, card in cards.items():
            req = {
                "game": RIFTBOUND,
                "tcgplayerId": tcgplayer_id,
                "condition": NEAR_MINT,
                "printing": (
                    NORMAL if card.classification.rarity in [COMMON, UNCOMMON] else FOIL
                ),
                "priceHistoryDuration": duration,
            }
            card_requests.append(req)

        chunks = [card_requests[i : i + 20] for i in range(0, len(card_requests), 20)]
        results: list[JustTCGCard] = []
        for chunk in chunks:
            chunk_results = self.get_with_retry(None, chunk)
            results.extend(chunk_results)

        self.logger.info(f"Retrieved {len(results)} cards from JustTCG")
        return results
