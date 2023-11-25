from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, ProductItem, Vendor

class Order(BusinessTimeAndUUIDStampedBaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name= "orders")
    placement_date = models.DateField()
    expected_receipt_date = models.DateField()
    actual_receipt_date = models.DateField(null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    qty_delayed = models.IntegerField()
    qty_defected = models.IntegerField()
    qty_accepted = models.IntegerField()


    def save(self, *args, **kwargs):
        if self.actual_receipt_date and not self.cost_price:
            self.cost_price= self.order_items.aggregate(cost_price= models.Sum("total_cost_price"))["cost_price"]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.product_item} from {self.vendor}- {self.business.id}"



class OrderItem(BusinessTimeAndUUIDStampedBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name= "order_items")
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name= "orders")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_cost_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.total_cost_price:
            self.total_cost_price= self.quantity * self.cost_price

        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.id} - {self.order} from {self.vendor}- {self.business.id}"
