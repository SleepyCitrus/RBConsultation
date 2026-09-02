import logging
from datetime import datetime, timezone

import boto3
from ingestion.justtcg.justtcg_card import JustTCGCard
from shared.logging.logger import logger
from shared.riftcodex.riftcodex_item import RiftcodexItem

dynamodb = boto3.resource("dynamodb")

CARD_METADATA_TABLE = "CardMetadata"
# TODO: V1 has historical information for a subset of cards, not sure what to do with
# it yet so bumping up the version and making a new table. Come back to this later
CARD_PRICE_TABLE = "CardPriceV2"


@logger
class DDBService:
    logger: logging.Logger

    def __init__(self):
        self.ddb = dynamodb

    def write_cards_metadata(self, cards: list[JustTCGCard]):
        table = self.ddb.Table(CARD_METADATA_TABLE)
        for card in cards:
            item = card.model_dump(
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
            table.put_item(Item=item)

    def write_cards_price(
        self, priced_cards: list[JustTCGCard], card_details: dict[str, RiftcodexItem]
    ):
        table = self.ddb.Table(CARD_PRICE_TABLE)

        rows_to_write = []
        for card in priced_cards:
            if card.variants:
                # We only want the pricing for the first variant which should be the lower rarity
                variant = card.variants[0]

                last_timestamp = datetime.min.replace(tzinfo=timezone.utc)
                item = {}

                for price_history in variant.priceHistory:
                    if price_history.t > last_timestamp:
                        last_timestamp = price_history.t
                        item = price_history.model_dump(include={"p", "t"})
                        item["name"] = card.name
                        item["tcgplayerId"] = card.tcgplayerId
                        item["rarity"] = card.rarity
                        item["set"] = card.set

                if item:
                    rows_to_write.append(item)

        self.logger.info(f"Writing {len(rows_to_write)} rows to DynamoDB")
        try:
            with table.batch_writer() as batch:
                for row in rows_to_write:
                    batch.put_item(Item=row)
        except Exception as e:
            self.logger.error(f"Error writing to DynamoDB: {e}")
