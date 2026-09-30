from app.providers import MockProvider


def test_mock_requirement_extracts_structured_input():
    result = MockProvider().extract("客户想采购20个900×1850×400灰白色钢制文件柜")
    assert result["quantity"] == 20
    assert result["width"] == 900
    assert result["height"] == 1850
    assert result["depth"] == 400
    assert result["provider_mode"] == "MOCK"


def test_mock_requirement_handoffs_incomplete_input():
    result = MockProvider().extract("请报价文件柜")
    assert result["handoff"] is True
