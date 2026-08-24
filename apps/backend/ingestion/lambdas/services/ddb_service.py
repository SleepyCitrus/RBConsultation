import boto3

from justtcg.justtcg_card import JustTCGCard

dynamodb = boto3.resource("dynamodb")

CARD_METADATA_TABLE = "CardMetadata"
CARD_PRICE_TABLE = "CardPrice"


class DDBService:
    def __init__(self):
        self.ddb = dynamodb

    def write_cards_metadata(self, cards: list[JustTCGCard]):
        table = self.ddb.Table(CARD_METADATA_TABLE)
        for card in cards:
            item = card.model_dump(
                include={"uuid", "id", "name", "game", "set", "set_name", "number", "rarity", "tcgplayerId", "details"}
            )
            table.put_item(Item=item)

    def write_cards_price(self, cards: list[JustTCGCard]):
        table = self.ddb.Table(CARD_PRICE_TABLE)

        rows_to_write = []
        for card in cards:
            if card.variants:
                # We only want the pricing for the first variant which should be the lower rarity
                variant = card.variants[0]

                for price_history in variant.priceHistory:
                    item = price_history.model_dump(include={"p", "t"})
                    item["name"] = card.name
                    rows_to_write.append(item)

        print(rows_to_write)
        try:
            with table.batch_writer() as batch:
                for row in rows_to_write:
                    batch.put_item(Item=row)
        except Exception as e:
            print(f"Error writing to DynamoDB: {e}")
