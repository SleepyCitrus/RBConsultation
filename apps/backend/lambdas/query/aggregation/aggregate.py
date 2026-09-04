from decimal import Decimal

from pydantic import BaseModel


class AggregatePrice(BaseModel):
    entries: int
    avg_price: Decimal
    total: Decimal


class AggregateSet(BaseModel):
    set_name: str
    # rarity -> prices
    averages: dict[str, AggregatePrice]
    total_entries: int
