from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


@dataclass
class JustTCGPriceHistory(BaseModel):
    p: Decimal = Field(decimal_places=2)
    t: datetime
