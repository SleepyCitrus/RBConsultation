from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, PlainSerializer


def auto_round_to_two_decimals(v: Decimal) -> Decimal:
    # Quantize forces exactly 2 decimal places immediately on input
    return v.quantize(Decimal("0.01"))


def epoch_to_datetime(value):
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    return value


EpochDatetime = Annotated[
    datetime,
    BeforeValidator(epoch_to_datetime),
    PlainSerializer(lambda dt: int(dt.timestamp()), return_type=int),
]
CurrencyDecimal = Annotated[Decimal, AfterValidator(auto_round_to_two_decimals)]
