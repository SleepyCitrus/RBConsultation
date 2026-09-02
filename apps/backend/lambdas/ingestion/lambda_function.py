import json

from ingestion.card_filter import CardFilter
from shared.riftcodex.riftcodex_service import RiftcodexService
from shared.services.ddb_service import DDBService
from shared.services.price_service import PriceService
from shared.services.riftbound_service import RiftboundService

rbService = RiftboundService()
priceService = PriceService(rbService)
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
    ddbService.write_cards_price(priced_cards, cards_to_price)

    return {"statusCode": 200, "body": json.dumps("Successful execution!")}
