import json

import boto3

from apps.backend.ingestion.lambdas.justtcg_card import JustTCGCard

dynamodb = boto3.resource("dynamodb")

CARD_PRICE_TABLE = "card-price"
CARD_METADATA_TABLE = "card-metadata"


class ddbService:
    def __init__(self):
        self.ddb = dynamodb

    def write_cards_metadata(self, cards: list[JustTCGCard]):
        table = self.ddb.Table(CARD_METADATA_TABLE)
        for card in cards:
            item = json.loads(
                card.model_dump_json(
                    include={
                        "uuid",
                        "id",
                        "name",
                        "game",
                        "set",
                        "set_name",
                        "number",
                        "rarity",
                        "tcgplayerId",
                        "details",
                    }
                )
            )
            table.put_item(Item=item)

    def write_cards_price(self, cards: list[JustTCGCard]):
        table = self.ddb.Table(CARD_PRICE_TABLE)
        for card in cards:
            if card.variants:
                # We only want the pricing for the first variant which should be the lower rarity
                variant = card.variants[0]

                for price_history in variant.priceHistory:
                    item = json.loads(price_history.model_dump_json(include={"p", "t"}))
                    item["card_name"] = card.name

                    table.put_item(Item=item)
