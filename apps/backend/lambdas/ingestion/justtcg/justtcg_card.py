from dataclasses import dataclass

from ingestion.justtcg.justtcg_variant import JustTCGVariant
from pydantic import BaseModel


@dataclass
class JustTCGCard(BaseModel):
    uuid: str
    id: str
    name: str
    game: str
    set: str
    set_name: str
    number: str
    rarity: str
    tcgplayerId: str
    variants: list[JustTCGVariant]

    # Optional fields
    mtgjsonId: str | None
    scryfallId: str | None
    details: str | None
