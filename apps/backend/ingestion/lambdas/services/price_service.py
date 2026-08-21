import os

import requests

from apps.backend.ingestion.lambdas.justtcg_card import JustTCGCard
from apps.backend.ingestion.lambdas.services.riftbound_service import RIFTBOUND, RiftboundService

GAMES_URL = "https://api.justtcg.com/v1/games"
CARDS_URL = "https://api.justtcg.com/v1/cards"


class PriceService:
    def __init__(self, rbService: RiftboundService):
        self.rbService = rbService

    def get_game_slugs(self):
        response = requests.get(GAMES_URL, headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]})

        response.raise_for_status()

        for game in response.json()["data"]:
            if game["id"].contains("riftbound"):
                print(game["id"], game["name"])

    def get_card(self):
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
                "priceHistoryDuration": "1y",
            },
        )
        response.raise_for_status()
        if response.json():
            print(response.json())

    def get_cards(self) -> list[JustTCGCard]:
        all_staples = self.rbService.get_staple_cards_dict()
        json_list = []
        for slug, staple in all_staples.items():
            temp = {
                "game": RIFTBOUND,
                "tcgplayerId": staple.tcgplayer_id,
                "condition": "NM",
                "printing": staple.printing,
                "priceHistoryDuration": "1y",
            }
            json_list.append(temp)

        chunks = [json_list[i : i + 20] for i in range(0, len(json_list), 20)]
        result: list[JustTCGCard] = []
        for chunk in chunks:
            response = requests.post(
                CARDS_URL,
                headers={"x-api-key": os.environ["JUSTTCG_API_KEY"], "Content-Type": "application/json"},
                json=chunk,
            )

            response.raise_for_status()
            if response.json():
                print(response.json())
                if response.json()["data"]:
                    for card in response.json()["data"]:
                        justtcg_card = JustTCGCard.model_validate(card)
                        # item = justtcg_card.model_dump_json(
                        #     include={"uuid", "id", "name", "game", "set", "set_name", "number", "rarity", "tcgplayerId"}
                        # )
                        result.append(justtcg_card)

        return result
