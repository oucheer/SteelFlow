import re


class MockProvider:
    mode = "MOCK"

    def extract(self, text: str):
        dimensions = re.search(r"(\d{3,4})\s*[×xX*]\s*(\d{3,4})\s*[×xX*]\s*(\d{3,4})", text)
        quantity = re.search(r"(\d+)\s*[个件台套]", text)
        if not dimensions or not quantity:
            return {"handoff": True, "reason": "缺少数量或完整尺寸，需人工确认", "provider_mode": self.mode}
        width, height, depth = map(int, dimensions.groups())
        return {"quantity": int(quantity[1]), "width": width, "height": height, "depth": depth,
                "color": "灰白" if "灰白" in text else "待确认", "configuration": "standard", "provider_mode": self.mode}


class DifyProvider:
    mode = "STUB"

    def extract(self, text: str):
        raise NotImplementedError("Dify 未配置；未启用真实模型")


class MaxKBProvider(DifyProvider):
    pass
