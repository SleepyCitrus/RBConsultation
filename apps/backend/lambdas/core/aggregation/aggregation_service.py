from decimal import Decimal

from shared.riftbound.riftbound_metadata import RIFTBOUND_SET_LABELS


class AggregationService:
    """
    Calculates the average price by rarity for a set.
    """

    def __init__(self): ...

    def get_aggregation_by_set(self, set: str) -> dict[str, Decimal]:
        if set not in RIFTBOUND_SET_LABELS:
            return {}

        return {}
