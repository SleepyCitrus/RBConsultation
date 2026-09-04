from dataclasses import dataclass

from ingestion.justtcg.justtcg_price_history import JustTCGPriceHistory
from pydantic import BaseModel
from shared.database.context_metadata import CurrencyDecimal, EpochDatetime


@dataclass
class JustTCGVariant(BaseModel):
    uuid: str
    id: str
    condition: str
    printing: str
    language: str
    tcgplayerSkuId: str
    price: CurrencyDecimal
    lastUpdated: EpochDatetime
    priceChange24hr: CurrencyDecimal | None
    priceHistory: list[JustTCGPriceHistory]

    # Unused
    # priceChange7d: float | None
    # avgPrice: float | None
