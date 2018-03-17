from wallet_models import Names, Products, Materials, Transactions
from typing import List
import peewee
from datetime import datetime, timedelta


class MaterialsL:
    material_id = None
    material_name = None
    quantity = None
    avg_price1 = None
    avg_price2 = None
    avg_price3 = None


MaterialsList = List[MaterialsL]


def _get_prices(mlist):
    pass


def get_materials_avg_price(product_id: int) -> MaterialsList:
    days3 = 3
    days7 = 7
    days_month = 30
    q_3day_avg_price = Transactions.select(
        peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy3"),
        Transactions.type_id
    ).group_by(Transactions.type_id) \
        .where(Transactions.date > datetime.now() - timedelta(days3)).alias("ab3")

    q_7day_avg_price = Transactions.select(
        peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy7"),
        Transactions.type_id
    ).group_by(Transactions.type_id) \
        .where(Transactions.date > datetime.now() - timedelta(days7)).alias("ab7")

    q_month_avg_price = Transactions.select(
        peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy30"),
        Transactions.type_id
    ).group_by(Transactions.type_id) \
        .where(Transactions.date > datetime.now() - timedelta(days_month)).alias("ab30")

    q_material_names = Materials.select(
        Materials.material_id.alias("material_id"), Names.name,
        q_month_avg_price.c.avg_buy30, Materials.quantity,
        q_7day_avg_price.c.avg_buy7, q_3day_avg_price.c.avg_buy3) \
        .join(Names, on=(Materials.material_id == Names.id))\
        .join(q_month_avg_price, peewee.JOIN.LEFT_OUTER, on=(q_month_avg_price.c.type_id == Materials.material_id))\
        .join(q_7day_avg_price, peewee.JOIN.LEFT_OUTER, on=(q_7day_avg_price.c.type_id == q_month_avg_price.c.type_id))\
        .join(q_3day_avg_price, peewee.JOIN.LEFT_OUTER, on=(q_3day_avg_price.c.type_id == q_7day_avg_price.c.type_id))\
        .where(Materials.product_id == product_id)
    qmn = q_material_names.alias("qmn1")
    l = list()
    for i in qmn:
        m = MaterialsL()
        # print("names test ", i.material_id, i.names.name)
        m.material_id = i.material_id
        m.material_name = i.names.name
        m.quantity = i.quantity
        if hasattr(i.names, "transactions"):
            # print("avg buy 30 ---> ", i.names.transactions.avg_buy30)
            m.avg_price1 = "{:,.2f}".format(i.names.transactions.avg_buy30)
            if hasattr(i.names.transactions, "transactions"):
                # print("avg buy 7 -------> ", i.names.transactions.transactions.avg_buy7)
                m.avg_price2 = "{:,.2f}".format(i.names.transactions.transactions.avg_buy7)
                if hasattr(i.names.transactions.transactions, "transactions"):
                    # print("avg buy 3 -------> ", i.names.transactions.transactions.transactions.avg_buy3)
                    m.avg_price3 = "{:,.2f}".format(i.names.transactions.transactions.transactions.avg_buy3)
        l.append(m)

    return l


def get_price_cost(l: MaterialsList) -> tuple:
    price_cost1=0
    price_cost2=0
    price_cost3=0

    for i in l:
        print(i.avg_price3)
        if i.avg_price1 is None:
            price_cost1 = None
        if i.avg_price2 is None:
            price_cost2 = None
        if i.avg_price3 is None:
            price_cost3 = None
        if price_cost1 is not None:
            price_cost1 += int(i.quantity)*float(i.avg_price1.replace(",", ""))
        if price_cost2 is not None:
            price_cost2 += int(i.quantity) * float(i.avg_price2.replace(",", ""))

        if price_cost3 is not None:
            price_cost3 += int(i.quantity) * float(i.avg_price3.replace(",", ""))
    if price_cost1 is not None:
        price_cost1 = "{:,.2f}".format(price_cost1)
    if price_cost2 is not None:
        price_cost2 = "{:,.2f}".format(price_cost2)
    if price_cost3 is not None:
        price_cost3 = "{:,.2f}".format(price_cost3)
    return price_cost1, price_cost2, price_cost3
