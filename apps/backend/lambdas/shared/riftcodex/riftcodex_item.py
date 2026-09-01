from typing import Optional

from pydantic import BaseModel


class RcAttributes(BaseModel):
    energy: int
    might: Optional[int]
    power: Optional[int]


class RcClassification(BaseModel):
    type: str
    supertype: Optional[str]
    rarity: str
    domain: list[str]


class RcText(BaseModel):
    rich: str
    plain: str
    flavour: str


class RcSet(BaseModel):
    set_id: str
    label: str


class RcMedia(BaseModel):
    image_url: str
    artist: str
    accessibility_text: str


class RcMetadata(BaseModel):
    clean_name: str
    updated_on: str
    alternate_art: bool
    overnumbered: bool
    signature: bool


# Some fields are commented out because they aren't relevant to determining the card
# price and are unnecessary bloat for Lambda execution purposes. Leaving them here
# for convenience so I don't need to recreate the pydantic model.
class RiftcodexItem(BaseModel):
    id: str
    name: str
    riftbound_id: str
    tcgplayer_id: str
    collector_number: int
    classification: RcClassification
    set: RcSet
    metadata: RcMetadata

    # attributes: RcAttributes
    # text: RcText
    # media: RcMedia
    # tags: list[str]
    # orientation: str
    # new: bool
