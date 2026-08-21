from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class JustTCGPriceHistory(BaseModel):
    p: float
    t: float
