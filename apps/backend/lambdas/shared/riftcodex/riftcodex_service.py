import json
import logging

import requests
from pydantic import TypeAdapter
from shared.logging.logger import logger
from shared.riftbound.riftbound_metadata import (
    OVERNUMBERED,
    RIFTBOUND_SET_IDS,
    SHOWCASE,
    SIGNATURE,
    SPECIAL_RARE,
    ULTIMATE,
)
from shared.riftcodex.riftcodex_item import RiftcodexItem


@logger
class RiftcodexService:
    """
    Service for interacting with the Riftcodex API.
    """

    logger: logging.Logger

    BASE_URL = "https://api.riftcodex.com"

    def convert_response(self, input: list) -> list[RiftcodexItem]:
        """
        Convert the response from Riftcodex to a list of RiftcodexItem objects.
        """
        codex_items = []

        for json_blob in input:
            try:
                if json_blob.get("tcgplayer_id", None):
                    converted_item = RiftcodexItem.model_validate(json_blob)

                    granular_rarity = self.get_granular_rarity(converted_item)
                    # Explicitly convert rarity to lowercase
                    converted_item.classification.rarity = granular_rarity.lower()
                    codex_items.append(converted_item)
            except Exception as e:
                self.logger.error(f"Error converting item: {e} - {json_blob}")

        return codex_items

    def get_granular_rarity(self, card: RiftcodexItem) -> str:
        """
        Determine the true granular rarity of a card. This is helpful if a card
        belongs in a bloated tier (e.g. showcase) but should be considered its own
        rarity (e.g. special art or ultimate)
        """

        catalog = card.riftbound_id.split("-")

        if len(catalog) == 3:

            # not a special rare, check if we are dealing with ON or signature
            card_number, catalog_number = catalog[1], catalog[2]

            if card_number.lower().startswith(SPECIAL_RARE.lower()):
                # Ahri, Inquisitive
                # ven-sp3-006
                return SPECIAL_RARE

            if (
                card_number.endswith("*")
                and card_number[:-1].isdigit()
                and catalog_number.isdigit()
                and int(card_number[:-1]) > int(catalog_number)
            ):
                # Yasuo - Unforgiven (Signature)
                # ogn-305*-298
                return SIGNATURE

            if (
                card_number.endswith("a")
                and card_number[:-1].isdigit()
                and catalog_number.isdigit()
                and int(card_number[:-1]) < int(catalog_number)
            ):
                # Fiora - Worthy (Alternate Art)
                # sfd-180a-221
                return SHOWCASE

            if (
                card_number.isdigit()
                and catalog_number.isdigit()
                and int(card_number) > int(catalog_number)
            ):
                name_lower = card.name.lower()

                if f"({ULTIMATE})" in name_lower:
                    # Baron Nashor (Ultimate)
                    # unl-238-219
                    return ULTIMATE
                return OVERNUMBERED

        return card.classification.rarity

    def get_all_cards(self) -> list[RiftcodexItem]:
        """
        Get all cards from Riftcodex.
        https://api.riftcodex.com/cards?sort=name&dir=1&set_id=ogn&page=1&size=100
        """

        results: list[RiftcodexItem] = []

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json",
        }

        for set in RIFTBOUND_SET_IDS:
            query_params = {
                "sort": "name",
                "dir": 1,
                "set_id": set,
                "size": 100,
                "page": 1,
            }

            while True:
                response = requests.get(
                    f"{self.BASE_URL}/cards", params=query_params, headers=headers
                )
                response.raise_for_status()

                items = self.convert_response(response.json()["items"])

                results.extend(items)

                if response.json()["pages"] > query_params["page"]:
                    query_params["page"] += 1
                else:
                    break

        self.logger.info(f"Retrieved {len(results)} cards from Riftcodex")
        return results


def test_granular_rarity():

    codex = RiftcodexService()
    with open("./../data/test_data_riftcodex.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        adapter = TypeAdapter(list[RiftcodexItem])
        items = adapter.validate_python(data["items"])

        for item in items:
            rarity = codex.get_granular_rarity(item)

            print(f"{item.name} rarity becomes {rarity}")
