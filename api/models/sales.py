from django.db import models
from api.models import ProductItem, Customer, BusinessTimeAndUUIDStampedBaseModel

class Sales(BusinessTimeAndUUIDStampedBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name= "sales")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def total_cost(self):
        self.sales_items.aggregrate(total_cost=  models.Sum("cost_price"))

class SalesItem(BusinessTimeAndUUIDStampedBaseModel):
    sales= models.ForeignKey(Sales, on_delete= models.CASCADE, related_name= "sales_items")
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name= "sales")
    quantity = models.IntegerField(default= 1)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.cost_price:
            self.cost_price = self.quantity * self.product_item.selling_price

        super().save(*args, **kwargs)
