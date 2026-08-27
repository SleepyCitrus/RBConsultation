from dataclasses import dataclass

from ingestion.justtcg.justtcg_shared import CurrencyDecimal, EpochDatetime
from pydantic import BaseModel


@dataclass
class JustTCGPriceHistory(BaseModel):
    p: CurrencyDecimal
    t: EpochDatetime
