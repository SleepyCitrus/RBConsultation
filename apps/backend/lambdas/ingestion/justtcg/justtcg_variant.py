from dataclasses import dataclass

from ingestion.justtcg.justtcg_price_history import JustTCGPriceHistory
from ingestion.justtcg.justtcg_shared import CurrencyDecimal, EpochDatetime
from pydantic import BaseModel


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
