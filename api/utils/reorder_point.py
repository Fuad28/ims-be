from django.db.models import QuerySet, Sum

from datetime import datetime, timedelta
from math import ceil

from api.enums import OrderStatusEnum
from api.models import ProductItem, OrderItem, SaleItem
from api.utils.model_inference import run_inference



def get_lead_time(product_item):
    order_items: QuerySet[OrderItem] = OrderItem.objects.filter(
        order__status=OrderStatusEnum.COMPLETED, 
        product_item=product_item
        ).order_by("order__placement_date").last(3)
    
    lead_time = 0

    for order_item in order_items:
        lead_time += (order_item.order.actual_receipt_date - order_item.order.placement_date).days

    return ceil(lead_time / 3)




def get_yesterdays_demand(product_item):
    """Gives demand on the given day"""

    yesterday = datetime.now().date() - timedelta(days=1)
    return  SaleItem.objects.filter(
        product_item=product_item, created_at=yesterday
        ).aggregate(demand= Sum("quantity"))["demand"]




def get_consumption_duration(product_item: ProductItem):
    """Computes how many days it takes to consume a particular quantity."""

    start_date = datetime.now().date()
    last_demand =  get_yesterdays_demand(product_item)
    daily_consumption = []
    todays_qty = product_item.quantity

    while todays_qty > 0:
        demand = run_inference(
            product_id=product_item.category.name,
            last_demand=last_demand,
            start_date=start_date,
        )

        daily_consumption.append(demand)
        todays_qty -= demand

        last_demand = demand
        start_date += timedelta(days=1)

    return daily_consumption, len(daily_consumption)





def get_lead_time_consumption(product_item: ProductItem):
    """Computes lead time consumption"""

    lead_time = get_lead_time(product_item)
    daily_consumption, days = get_consumption_duration(product_item)
    last_nth_days_consumption = daily_consumption[-lead_time:]
    
    return sum(last_nth_days_consumption)




def compute_reorder_point(product_item: ProductItem):
    return product_item.safety_stock + get_lead_time_consumption(product_item)