import json

from apps.backend.ingestion.lambdas.services.price_service import PriceService
from apps.backend.ingestion.lambdas.services.riftbound_service import RiftboundService

rbService = RiftboundService()
priceService = PriceService(rbService)


def lambda_handler(event, context):
    cards = priceService.get_cards()
    return {"statusCode": 200, "body": json.dumps("Successful execution!")}
