from wallet_models import Names, Products, Materials, Transactions
from typing import List
import peewee
from datetime import datetime, timedelta


class MaterialsL:
    material_id = None


MaterialsList = List[MaterialsL]


def _get_prices(mlist):
    pass


def get_materials(product_id: int) -> MaterialsList:
    m = Materials()
    days3 = 3
    days7 = 7
    days_month = 30
    q_3day_avg_price = Transactions.select(
        peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy3"),
        Transactions.type_id
    ).group_by(Transactions.type_id) \
        .where(Transactions.date > datetime.now() - timedelta(1)).alias("ab3")

    q_7day_avg_price = Transactions.select(
        peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy7"),
        Transactions.type_id
    ).group_by(Transactions.type_id) \
        .where(Transactions.date > datetime.now() - timedelta(days7)).alias("ab7")

    q_material_names = Materials.select(
        Materials.material_id.alias("material_id"), Names.name,
        q_7day_avg_price.c.avg_buy7, q_3day_avg_price.c.avg_buy3) \
        .join(Names, on=(Materials.material_id == Names.id))\
        .join(q_7day_avg_price, peewee.JOIN.LEFT_OUTER, on=(q_7day_avg_price.c.type_id == Materials.material_id))\
        .join(q_3day_avg_price, peewee.JOIN.LEFT_OUTER, on=(q_3day_avg_price.c.type_id == q_7day_avg_price.c.type_id))\
        .where(Materials.product_id == product_id)
    qmn = q_material_names.alias("qmn1")
    for i in qmn:
        print("names test ", i.material_id, i.names.name)
        if hasattr(i.names, "transactions"):
            print("avg buy 7 ---> ", i.names.transactions.avg_buy7)
            if hasattr(i.names.transactions, "transactions"):
                print("avg buy 3 -------> ",i.names.transactions.transactions.avg_buy3)



    return []
