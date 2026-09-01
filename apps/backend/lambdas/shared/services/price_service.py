import logging
import os

import requests
from ingestion.justtcg.justtcg_card import JustTCGCard
from shared.logging.logger import logger
from shared.riftcodex.riftcodex_item import RiftcodexItem
from shared.services.riftbound_service import (
    COMMON,
    FOIL,
    NORMAL,
    RIFTBOUND,
    UNCOMMON,
    RiftboundService,
)

GAMES_URL = "https://api.justtcg.com/v1/games"
CARDS_URL = "https://api.justtcg.com/v1/cards"


@logger
class PriceService:
    logger: logging.Logger

    def __init__(self, rbService: RiftboundService):
        self.rbService = rbService

    def get_game_slugs(self):
        response = requests.get(
            GAMES_URL, headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]}
        )

        response.raise_for_status()

        for game in response.json()["data"]:
            if game["id"].contains("riftbound"):
                self.logger.info(f"Found game: {game['id']} - {game['name']}")
                return game["id"]

    def get_card(self, duration: str = "7d"):
        """
        Test function to get a single card.
        If getting multiple cards, use get_cards() instead.
        """

        response = requests.get(
            CARDS_URL,
            headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]},
            params={
                "game": RIFTBOUND,
                # "cardId": get_card_slug("defy", ORIGINS, COMMON),
                "tcgplayerId": "652814",
                "condition": "NM",
                "printing": "Normal",
                "priceHistoryDuration": duration,
            },
        )
        response.raise_for_status()
        if response.json():
            print(response.json())

    def get_prices(
        self, cards: dict[str, RiftcodexItem], duration: str = "7d"
    ) -> list[JustTCGCard]:
        card_requests = []
        for tcgplayer_id, card in cards.items():
            req = {
                "game": RIFTBOUND,
                "tcgplayerId": tcgplayer_id,
                "condition": "NM",
                "printing": (
                    NORMAL if card.classification.rarity in [COMMON, UNCOMMON] else FOIL
                ),
                "priceHistoryDuration": duration,
            }
            card_requests.append(req)

        chunks = [card_requests[i : i + 20] for i in range(0, len(card_requests), 20)]
        results: list[JustTCGCard] = []
        for chunk in chunks:
            response = requests.post(
                CARDS_URL,
                headers={
                    "x-api-key": os.environ["JUSTTCG_API_KEY"],
                    "Content-Type": "application/json",
                },
                json=chunk,
            )

            response.raise_for_status()
            if response.json():
                if response.json()["data"]:
                    for card in response.json()["data"]:
                        justtcg_card = JustTCGCard.model_validate(card)
                        results.append(justtcg_card)

        self.logger.info(f"Retrieved {len(results)} cards from JustTCG")
        return results
