import json

from apps.backend.ingestion.lambdas.services.ddb_service import DDBService
from apps.backend.ingestion.lambdas.services.price_service import PriceService
from apps.backend.ingestion.lambdas.services.riftbound_service import RiftboundService

rbService = RiftboundService()
priceService = PriceService(rbService)
ddbService = DDBService()


def lambda_handler(event, context):
    cards = priceService.get_cards()
    ddbService.write_cards_price(cards)

    return {"statusCode": 200, "body": json.dumps("Successful execution!")}
