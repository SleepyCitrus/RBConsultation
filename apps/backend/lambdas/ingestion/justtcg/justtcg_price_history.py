from dataclasses import dataclass

from pydantic import BaseModel
from shared.database.context_metadata import CurrencyDecimal, EpochDatetime


@dataclass
class JustTCGPriceHistory(BaseModel):
    p: CurrencyDecimal
    t: EpochDatetime
