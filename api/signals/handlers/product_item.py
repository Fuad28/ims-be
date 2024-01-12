from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from api.models import ProductItem
from api.utils.model_inference import run_inference, compute_eoq
from api.utils.reorder_point import compute_reorder_point, get_yesterdays_demand

@receiver(post_save, sender= ProductItem)
def handle_product_save(sender, **kwargs):
    product_item: ProductItem= kwargs["instance"]

    compute= False

    if not product_item.last_forcast:
        compute= True 
    
    elif product_item.last_forcast.year != timezone.now().year:
        compute= True

    if compute:

        product_item.annual_demand, _= run_inference(
            product_id= product_item.category.name,
            last_demand= get_yesterdays_demand(product_item)
        )
        
        product_item.eoq= compute_eoq(
            demand= product_item.annual_demand, 
            unit_cost= product_item.cost_price,
            ordering_cost= product_item.ordering_cost,
            holding_cost= product_item.holding_cost
        )

        product_item.reordering_point= compute_reorder_point(product_item)

        product_item.last_forcast= timezone.now()
        
        product_item.save()