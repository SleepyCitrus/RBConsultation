import logging
from collections import defaultdict
from decimal import Decimal
from typing import Optional

from query.aggregation.aggregate import AggregatePrice, AggregateSet
from shared.database.ddb_service import DDBService
from shared.logging.logger import logger
from shared.riftbound.riftbound_metadata import RIFTBOUND_SET_CAPITALIZED_LABELS


@logger
class AggregationService:
    """
    Calculates the average price by rarity for a set.
    """

    logger: logging.Logger

    def __init__(self, ddbService: DDBService):
        self.ddbService = ddbService

    def get_aggregation_by_set(self, set_name: str) -> Optional[AggregateSet]:
        if set_name not in RIFTBOUND_SET_CAPITALIZED_LABELS:
            self.logger.info(
                f"Invalid set name: {set_name} not in {RIFTBOUND_SET_CAPITALIZED_LABELS}"
            )
            return None

        card_prices = self.ddbService.query_prices(set_name=set_name, rarity=None)

        averages = defaultdict(
            lambda: AggregatePrice(entries=0, avg_price=Decimal(0), total=Decimal(0))
        )

        for card_price in card_prices:
            card_avg = averages[card_price.rarity]
            card_avg.entries += 1
            card_avg.total += card_price.p
            card_avg.avg_price = round(card_avg.total / card_avg.entries, 2)

        total_entries = 0
        for _, v in averages.items():
            total_entries += v.entries

        aggregate_set = AggregateSet(
            set_name=set_name, total_entries=total_entries, averages=averages
        )

        return aggregate_set
