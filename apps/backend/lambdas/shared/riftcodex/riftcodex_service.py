import logging

import requests
from pydantic import TypeAdapter
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
        adapter = TypeAdapter(list[RiftcodexItem])
        return adapter.validate_python(input)

    def get_all_cards(self) -> list[RiftcodexItem]:
        """
        Get all cards from Riftcodex.
        https://api.riftcodex.com/cards?sort=name&dir=1&set_id=ogn&page=1&size=100
        """

        results: list[RiftcodexItem] = []

        for set in RIFTBOUND_SETS:
            query_params = {
                "sort": "name",
                "dir": "1",
                "set_id": set,
                "size": 100,
                "page": 1,
            }

            while True:
                response = requests.get(f"{self.BASE_URL}/cards", params=query_params)
                response.raise_for_status()

                items = self._convert_response(response.json()["items"])

                print(items)
                results.extend(items)

                if response.json()["pages"] > query_params["page"]:
                    query_params["page"] += 1
                else:
                    break

        self.logger.info(f"Retrieved {len(results)} cards from Riftcodex")
        return results
