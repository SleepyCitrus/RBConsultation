from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, PlainSerializer


def auto_round_to_two_decimals(v: Decimal) -> Decimal:
    # Quantize forces exactly 2 decimal places immediately on input
    return v.quantize(Decimal("0.01"))


EpochDatetime = Annotated[datetime, PlainSerializer(lambda dt: int(dt.timestamp()), return_type=int)]
CurrencyDecimal = Annotated[
    Decimal, AfterValidator(auto_round_to_two_decimals), PlainSerializer(lambda d: f"{d:.2f}", return_type=str)
]
