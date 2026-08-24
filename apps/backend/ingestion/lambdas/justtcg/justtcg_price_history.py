from dataclasses import dataclass

from pydantic import BaseModel

from justtcg.shared import CurrencyDecimal, EpochDatetime


@dataclass
class JustTCGPriceHistory(BaseModel):
    p: CurrencyDecimal
    t: EpochDatetime
