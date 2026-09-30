from datetime import timedelta, date
from sqlalchemy import select
from pwdlib import PasswordHash

from .models import *
from .services import Service
from .config import settings

READS = ["customer.read", "product.read", "quote.read", "contract.read", "order.read", "conversation.read", "production.read", "dashboard.read", "approval.read"]


def seed():
    with Session() as db:
        if db.get(Organization, "demo"):
            print("Seed already exists; preserved.")
            return
        db.add(Organization(id="demo", name="钢制家具 · 演示企业"))
        db.flush()
        roles = {"admin": (["*"], "organization"), "sales": (READS + ["customer.write", "quote.write", "contract.write", "order.write", "conversation.write"], "organization"),
                 "support": (READS + ["conversation.write"], "organization"), "supervisor": (READS + ["plan.write", "plan.approve", "report.write"], "organization"),
                 "worker": (["production.read", "report.write"], "assigned"), "manager": (READS + ["quote.approve", "order.approve", "plan.approve", "audit.read"], "organization")}
        for role, (permissions, scope) in roles.items():
            db.add(Role(id=role, permissions=permissions, scope=scope))
        db.flush()
        names = [("admin", "系统管理员", "admin"), ("sales1", "张三", "sales"), ("sales2", "李文", "sales"),
                 ("sales3", "王静", "sales"), ("sales4", "陈杰", "sales"), ("sales5", "赵敏", "sales"),
                 ("support", "客服小林", "support"), ("supervisor", "生产主管", "supervisor"), ("worker", "张工", "worker"), ("manager", "经营负责人", "manager")]
        password_hash = PasswordHash.recommended().hash(settings.seed_password)
        for username, name, role in names:
            db.add(User(id=username, org_id="demo", username=username, name=name, role_id=role, password_hash=password_hash))
        db.flush()
        admin, sales, manager, supervisor = (db.get(User, x) for x in ("admin", "sales1", "manager", "supervisor"))
        service = Service(db, sales, "seed")
        reviewer = Service(db, manager, "seed")
        production = Service(db, supervisor, "seed")
        sources = ["淘宝", "京东", "抖音", "小红书", "拼多多", "微信"]
        customers = []
        for i, name in enumerate(["上海聚联科技", "杭州铭意商贸", "广州林办公室", "深圳集公科技", "成都森泰家具", "北京嘉瑞集团", "南京启明教育", "苏州远航实业", "武汉蓝谷医疗", "合肥新创办公"]):
            customer = service.customer({"name": name, "contact": ["张先生", "李女士", "王先生"][i % 3], "phone": f"138000000{i:02d}",
                                         "source": sources[i % 6], "level": "B", "tags": ["企业采购"], "identities": []})
            customers.append(customer)
        routing = [{"name": name, "capacity": capacity, "work_center": center} for name, capacity, center in
                   [("下料", 120, "激光切割"), ("冲压", 100, "冲压中心"), ("折弯", 80, "折弯中心"), ("焊接", 60, "焊接中心"), ("喷涂", 90, "喷涂线"), ("装配质检", 70, "装配中心")]]
        products = []
        for i in range(20):
            category = ["文件柜", "更衣柜", "密集架", "办公桌"][i % 4]
            product = Product(id=f"product-{i+1}", org_id="demo", name=f"{['钢制双门', '多门', '移动式', '简约'][i % 4]}{category}" + (f" {i//4+1}型" if i >= 4 else ""),
                              category=category, attributes={"width": 900, "height": 1850, "depth": 400, "thickness": "0.8mm", "material": "冷轧钢", "color": "灰白", "surface": "静电喷涂", "demo": True},
                              bom=[{"material": "冷轧钢板", "quantity": "24", "unit": "kg"}, {"material": "锁具", "quantity": "1", "unit": "套"}], routing=routing)
            db.add(product)
            db.flush()
            products.append(product)
            db.add(PriceRule(org_id="demo", product_id=product.id, rule_version=f"DEMO-2026-{i+1:03}", effective_at=now() - timedelta(days=1),
                             priority=1, config={"base": str(420 + (i % 4) * 180), "dimension_rate": "100", "reinforced": "80", "quantity_threshold": 20,
                                                 "quantity_discount": "0.03", "levels": {"A": "0.02", "B": "0", "C": "0"}}))
            for j in range(3 if i < 10 else 2):
                db.add(SKU(org_id="demo", product_id=product.id, code=f"ST-{i+1:03}-{j+1}", attributes={"color": ["灰白", "浅灰", "黑色"][j]}))
        db.flush()
        for i in range(20):
            text = "需要20个900×1850×400灰白钢制文件柜，请提供报价。"
            db.add(Conversation(org_id="demo", customer_id=customers[i % 10]["id"], messages=[{"role": "customer", "text": text},
                                {"role": "assistant", "text": "已提取需求，请确认后生成报价草稿。", "mode": "MOCK"}],
                                requirement={"quantity": 20, "width": 900, "height": 1850, "depth": 400, "color": "灰白", "configuration": "standard", "provider_mode": "MOCK"}))
        for i in range(10):
            data = {"customer_id": customers[i]["id"], "product_id": products[i % 4].id, "quantity": 20 + i * 5,
                    "width": 900, "height": 1850, "depth": 400, "color": "灰白", "configuration": "standard", "logistics": "0", "other": "0"}
            quote = service.quote(data)
            if i >= 5:
                continue
            approval = service.approval("quote", quote["id"])
            reviewer.decision(approval["id"], True)
            service.quote_state(quote["id"], "sent")
            service.quote_state(quote["id"], "accepted")
            service.contract(quote["id"])
            order = service.order(quote["id"])
            if i >= 3:
                continue
            approval = service.approval("order", order["id"])
            reviewer.decision(approval["id"], True)
            plan = service.submit_order(order["id"])
            approval = production.approval("plan", plan["id"])
            reviewer.decision(approval["id"], True)
            production.publish(plan["id"])
            works = list(db.scalars(select(WorkOrder).where(WorkOrder.plan_id == plan["id"]).order_by(WorkOrder.sequence)))
            for work in works[:6 if i == 0 else 2]:
                production.report(work.id, {"actual": 10, "qualified": 10, "rejected": 0, "hours": "2", "remark": "演示报工", "date": date.today().isoformat()})
        db.commit()
        print("Seed created: 20 products, 50 SKUs, 10 customers, 10 quotes, 5 orders, 3 plans, 10 reports, 20 conversations.")


if __name__ == "__main__":
    seed()
