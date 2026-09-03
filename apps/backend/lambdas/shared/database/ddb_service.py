import logging
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key
from ingestion.justtcg.justtcg_card import JustTCGCard
from shared.logging.logger import logger
from shared.riftbound.riftbound_metadata import RIFTBOUND_SET_CAPITALIZED_LABELS

dynamodb = boto3.resource("dynamodb", region_name="us-west-1")

CARD_METADATA_TABLE = "CardMetadata"
# TODO: V1 has historical information for a subset of cards, not sure what to do with
# it yet so bumping up the version and making a new table. Come back to this later
CARD_PRICE_TABLE = "CardPriceV2"
PRICE_BY_RARITY_GSI = "Price_By_Set_Rarity"


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

    def query_prices(self, set: str):
        """
        Get prices by set from the prices table GSI.
        """
        self.logger.info(f"Querying prices from DynamoDB")

        table = self.ddb.Table(CARD_PRICE_TABLE)

        if set in RIFTBOUND_SET_CAPITALIZED_LABELS:

            items = []
            last_evaluated_key = None

            while True:
                query_params = {
                    "IndexName": PRICE_BY_RARITY_GSI,
                    "KeyConditionExpression": Key("set").eq(set),
                }

                if last_evaluated_key:
                    query_params["ExclusiveStartKey"] = last_evaluated_key

                response = table.query(**query_params)

                # 4. Extract and print the returned items
                items.extend(response.get("Items", []))

                last_evaluated_key = response.get("LastEvaluatedKey", None)
                if not last_evaluated_key:
                    break

            print(f"Retrieved {len(items)} items from GSI.")
            return items

    def batch_write_prices(self, rows_to_write: list[dict[str, Any]]):
        self.logger.info(f"Writing {len(rows_to_write)} rows to DynamoDB")

        table = self.ddb.Table(CARD_PRICE_TABLE)

        try:
            with table.batch_writer() as batch:
                for row in rows_to_write:
                    batch.put_item(Item=row)
        except Exception as e:
            self.logger.error(f"Error writing to DynamoDB: {e}")
