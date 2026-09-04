from pydantic import BaseModel
from shared.database.context_metadata import CurrencyDecimal


class AggregatePrice(BaseModel):
    entries: int
    avg_price: CurrencyDecimal
    total: CurrencyDecimal


class AggregateSet(BaseModel):
    set_name: str
    # rarity -> prices
    averages: dict[str, AggregatePrice]
    total_entries: int
