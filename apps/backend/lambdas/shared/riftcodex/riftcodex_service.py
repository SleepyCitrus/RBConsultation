import logging

import requests
from shared.logging.logger import logger
from shared.riftcodex.riftcodex_item import RiftcodexItem
from shared.services.riftbound_service import RIFTBOUND_SETS


@logger
class RiftcodexService:
    """
    Service for interacting with the Riftcodex API.
    """

    logger: logging.Logger

    BASE_URL = "https://api.riftcodex.com"

    def _convert_response(self, input: list) -> list[RiftcodexItem]:
        """
        Convert the response from Riftcodex to a list of RiftcodexItem objects.
        """
        codex_items = []

        for json_blob in input:
            try:
                if json_blob.get("tcgplayer_id", None):
                    converted_item = RiftcodexItem.model_validate(json_blob)
                    codex_items.append(converted_item)
            except Exception as e:
                self.logger.error(f"Error converting item: {e} - {json_blob}")

        return codex_items

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

        for set in RIFTBOUND_SETS:
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

                items = self._convert_response(response.json()["items"])

                results.extend(items)

                if response.json()["pages"] > query_params["page"]:
                    query_params["page"] += 1
                else:
                    break

        self.logger.info(f"Retrieved {len(results)} cards from Riftcodex")
        return results
