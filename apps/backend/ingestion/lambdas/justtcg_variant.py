from dataclasses import dataclass

from pydantic import BaseModel

from apps.backend.ingestion.lambdas.justtcg_price_history import JustTCGPriceHistory


@dataclass
class JustTCGVariant(BaseModel):
    uuid: str
    id: str
    condition: str
    printing: str
    language: str
    tcgplayerSkuId: str
    price: float
    lastUpdated: float
    priceChange24hr: float | None
    priceHistory: list[JustTCGPriceHistory]

    # Unused
    # priceChange7d: float | None
    # avgPrice: float | None
