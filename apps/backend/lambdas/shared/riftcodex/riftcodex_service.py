import logging

import requests
from shared.logging.logger import logger
from shared.riftbound.riftbound_metadata import (
    OVERNUMBERED,
    RIFTBOUND_SET_IDS,
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
                # e.g. Ahri, Inquisitive (ven-sp3-006)
                return SPECIAL_RARE

            if (
                card_number.isdigit()
                and catalog_number.isdigit()
                and int(card_number) > int(catalog_number)
            ):
                name_lower = card.name.lower()

                if f"({SIGNATURE})" in name_lower:
                    return SIGNATURE
                elif f"({ULTIMATE})" in name_lower:
                    return ULTIMATE
                else:
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
