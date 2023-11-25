from django.db import models
from api.models import BusinessTimeAndUUIDStampedBaseModel, ProductItem

class Vendor(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    qdp_rating = models.FloatField()

    @property
    def products(self):
        product_items_ids= [order.product_item.id for order in self.orders.select_related("produt_item")]

        ProductItem.objects.filter(id__in= product_items_ids )


    def __str__(self):
        return f"{self.id} - {self.name} - {self.qdp_rating}"
    

