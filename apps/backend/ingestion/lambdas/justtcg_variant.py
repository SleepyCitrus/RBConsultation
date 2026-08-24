from dataclasses import dataclass

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from justtcg_price_history import JustTCGPriceHistory


@dataclass
class JustTCGVariant(BaseModel):
    uuid: str
    id: str
    condition: str
    printing: str
    language: str
    tcgplayerSkuId: str
    price: Decimal = Field(decimal_places=2)
    lastUpdated: datetime
    priceChange24hr: Decimal | None = Field(decimal_places=2)
    priceHistory: list[JustTCGPriceHistory]

    # Unused
    # priceChange7d: float | None
    # avgPrice: float | None
