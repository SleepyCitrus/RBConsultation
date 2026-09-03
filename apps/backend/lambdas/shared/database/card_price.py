from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CardPrice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    set: str
    rarity: str
    p: Decimal
    t: int
    tcgplayer_id: int = Field(alias="tcgplayerId")
