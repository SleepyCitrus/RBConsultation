from pydantic import BaseModel, ConfigDict, Field
from shared.database.context_metadata import CurrencyDecimal


class CardPrice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    set: str
    rarity: str
    p: CurrencyDecimal
    t: int
    tcgplayer_id: int = Field(alias="tcgplayerId")
