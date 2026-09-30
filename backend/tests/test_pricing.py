from app.pricing import calculate


RULE = {"base": "420", "dimension_rate": "100", "reinforced": "80", "quantity_threshold": 20,
        "quantity_discount": "0.03", "levels": {"A": "0.02", "B": "0"}}
DATA = {"quantity": 20, "width": 900, "height": 1850, "depth": 400, "configuration": "standard", "logistics": "0", "other": "0"}


def test_pricing_is_replayable_and_exact():
    first = calculate(DATA, RULE, "B", "DEMO-1")
    second = calculate(DATA, RULE, "B", "DEMO-1")
    assert first == second
    assert first["total"] == "8148.00"
    assert first["breakdown"]["quantity_discount"] == "252.00"


def test_pricing_includes_customer_discount():
    result = calculate(DATA, RULE, "A", "DEMO-1")
    assert result["customer_level"] == "A"
    assert result["total"] == "7985.04"
