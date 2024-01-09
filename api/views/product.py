from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from api.models import Product, ProductItem
from api.serializers.product import ProductSerializer, ProductItemSerializer
from api.utils.model_inference import compute_eoq, run_inference
from api.utils.reorder_point import get_yesterdays_demand, compute_reorder_point


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(business=self.request.user.business)


class ProductItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductItemSerializer

    def get_queryset(self):
        return ProductItem.objects.filter(business=self.request.user.business)
    
    def retrieve(self, request, *args, **kwargs):
        product_item: ProductItem= self.get_object()

        if product_item.last_forcast:
            if product_item.last_forcast.year != timezone.now().year:

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

                product_item.save()
                
        return super().retrieve(request, *args, **kwargs)
