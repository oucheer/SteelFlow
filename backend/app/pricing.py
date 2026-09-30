from decimal import Decimal, ROUND_HALF_UP


def money(value):
    return str(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate(data: dict, rule: dict, level: str, version: str):
    qty = Decimal(data["quantity"])
    base = Decimal(rule["base"])
    volume = Decimal(data["width"] * data["height"] * data["depth"]) / Decimal(900 * 1850 * 400)
    dimension = max(Decimal(0), volume - 1) * Decimal(rule["dimension_rate"])
    configuration = Decimal(rule["reinforced"]) if data["configuration"] == "reinforced" else Decimal(0)
    subtotal = (base + dimension + configuration) * qty
    quantity_discount = subtotal * Decimal(rule["quantity_discount"]) if qty >= rule["quantity_threshold"] else Decimal(0)
    customer_discount = (subtotal - quantity_discount) * Decimal(rule["levels"].get(level, "0"))
    parts = {
        "base": money(base * qty), "dimension": money(dimension * qty),
        "configuration": money(configuration * qty), "quantity_discount": money(quantity_discount),
        "customer_discount": money(customer_discount), "logistics": money(data["logistics"]), "other": money(data["other"]),
    }
    total = sum(Decimal(parts[k]) for k in ("base", "dimension", "configuration", "logistics", "other"))
    total -= Decimal(parts["quantity_discount"]) + Decimal(parts["customer_discount"])
    return {"total": money(total), "unit_price": money(total / qty), "breakdown": parts, "rule_version": version, "customer_level": level}
