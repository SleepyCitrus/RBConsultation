import logging

from shared.logging.logger import logger
from shared.riftbound.riftbound_metadata import (
    BATTLEFIELD,
    EPIC,
    LEGEND,
    RARE,
    SHOWCASE_RARITY_TIERS,
    UNCOMMON,
)
from shared.riftcodex.riftcodex_item import RiftcodexItem

RARITY_SETS = {UNCOMMON: [UNCOMMON, RARE], EPIC: [EPIC, *SHOWCASE_RARITY_TIERS]}


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
            card_rarity = card.classification.rarity.lower()

            if (
                card.classification.type == LEGEND
                and card_rarity not in SHOWCASE_RARITY_TIERS
            ):
                # Skip regular legend cards
                continue
            elif card.classification.type == BATTLEFIELD:
                # Skip battlefield cards since they're usually not worth anything
                continue

            if card_rarity in rarity_set and card.tcgplayer_id not in filtered_cards:
                filtered_cards[card.tcgplayer_id] = card

        self.logger.info(
            f"Filtered {len(filtered_cards)} cards for rarity {rarity_set}: {[card.name for _, card in filtered_cards.items()]}"
        )
        return filtered_cards
