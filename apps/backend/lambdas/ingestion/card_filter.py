import logging

from shared.logging.logger import logger
from shared.riftcodex.riftcodex_item import RiftcodexItem
from shared.services.riftbound_service import EPIC, RARE, SHOWCASE, UNCOMMON

RARITY_SETS = {UNCOMMON: [UNCOMMON, RARE], EPIC: [EPIC, SHOWCASE]}


@logger
class CardFilter:

    logger: logging.Logger

    def filter_cards(
        self, cards: list[RiftcodexItem], rarity: str
    ) -> dict[str, RiftcodexItem]:
        """
        Filter cards based on rarity.

        Returns:
            dict[str, RiftcodexItem]: A dictionary of filtered cards with tcgplayer_id as the key.
        """
        filtered_cards: dict[str, RiftcodexItem] = {}

        rarity_set = []

        if rarity not in RARITY_SETS:
            return {}
        else:
            rarity_set = RARITY_SETS[rarity]

        for card in cards:
            if card.classification.rarity in rarity_set and rarity == "epic":
                if card.classification.rarity == "rare" and not (
                    card.metadata.signature or card.metadata.overnumbered
                ):
                    # regular legend can skip
                    continue
                else:
                    if card.tcgplayer_id not in filtered_cards:
                        filtered_cards[card.tcgplayer_id] = card
            elif card.classification.rarity in rarity_set and rarity == "uncommon":
                if card.tcgplayer_id not in filtered_cards:
                    filtered_cards[card.tcgplayer_id] = card

        self.logger.info(f"Filtered {len(filtered_cards)} cards for rarity {rarity}")
        return filtered_cards
