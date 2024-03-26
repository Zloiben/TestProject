from decimal import Decimal, ROUND_HALF_UP


def format_decimal(value: Decimal) -> str:
    normalized_value = value.normalize()
    if normalized_value == normalized_value.to_integral():
        return str(normalized_value.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
    return str(normalized_value.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
