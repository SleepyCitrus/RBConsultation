import json
from datetime import datetime, timezone

from ingestion.card_filter import CardFilter
from ingestion.justtcg.justtcg_card import JustTCGCard
from shared.database.ddb_service import DDBService
from shared.riftcodex.riftcodex_item import RiftcodexItem
from shared.riftcodex.riftcodex_service import RiftcodexService
from shared.services.catalog_service import CatalogService
from shared.services.price_service import PriceService

catalogService = CatalogService()
priceService = PriceService(catalogService)
ddbService = DDBService()
riftcodexService = RiftcodexService()


def lambda_handler(event, context):
    all_cards = riftcodexService.get_all_cards()

    # Some math regarding why certain cards will be disregarded for price checking:

    # 288 common
    # 256 uncommon
    # 249 rare - 45 legends can be ignored so 204 rare
    # 143 epic
    # 259 showcase  <- epic and show

    # The limitations of JustTCG's free tier is 100 daily requests and 1000 monthly requests. Requests can be
    # batched in groups of 20 cards per request.

    # Commons can be ignored completely, the most expensive card is defy at ~$5 which is mostly negligible

    # Uncommon and rares can be checked less frequently. If we check every 3 days then that would require:
    # 256 + 204 = 460 / 20 = ~23 requests / 3 days -> ~8 requests / day = 230-253 requests / month

    # Epic and showcase cards are the main driving factor for box EV which means they should be checked more frequently
    # for price swings. If we check every 2 days then that would require:
    # 143 + 259 = 402 / 20 = ~21 requests / 2 days -> ~11 requests / day = 315 requests / month

    # In total this would require approximately 545 - 568 requests / month which keeps us well within the free tier.

    process_rarity = event.get("rarity", "")

    if not process_rarity:
        return {
            "statusCode": 500,
            "body": json.dumps("Missing rarity in event detail!"),
        }

    cards_to_price = CardFilter().filter_cards(all_cards, process_rarity)

    priced_cards = priceService.get_prices(cards_to_price, duration="7d")
    write_cards_price(priced_cards, cards_to_price)

    return {"statusCode": 200, "body": json.dumps("Successful execution!")}


def write_cards_price(
    priced_cards: list[JustTCGCard], card_details: dict[str, RiftcodexItem]
):
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
                    if card_details.get(card.tcgplayerId, ""):
                        item["rarity"] = card_details[
                            card.tcgplayerId
                        ].classification.rarity.capitalize()
                    else:
                        item["rarity"] = card.rarity.capitalize()
                    item["set"] = card.set_name

            if item:
                rows_to_write.append(item)

    ddbService.batch_write_prices(rows_to_write=rows_to_write)
