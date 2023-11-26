from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, ProductItem, Vendor

class Order(BusinessTimeAndUUIDStampedBaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name= "orders")
    placement_date = models.DateField(auto_now_add= True)
    expected_receipt_date = models.DateField()
    actual_receipt_date = models.DateField(null=True, blank=True)
    total_cost_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)


    def compute_qdp(self):
        QUALITY_PERC, DELIVERY_PERC= 60, 40
        order_items: models.QuerySet[OrderItem]=  self.order_items
        qdp= 0

        for item in order_items:
            qdp += QUALITY_PERC * (item.qty_defected/item.qty_ordered) + DELIVERY_PERC * (item.qty_delayed/item.qty_ordered)

        return qdp
    

    @property
    def order_items(self) -> models.QuerySet:
        return self.order_items.all()

    def __str__(self):
        return f"{self.id} - {self.vendor} - {self.placement_date}"



class OrderItem(BusinessTimeAndUUIDStampedBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name= "order_items")
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name= "orders")
    unit_cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty_ordered = models.IntegerField()
    qty_delayed = models.IntegerField(default= 0)
    qty_defected = models.IntegerField(default= 0)
    qty_accepted = models.IntegerField(default= 0)
    

    def save(self, *args, **kwargs):
        self.cost_price= self.qty_ordered * self.unit_cost_price

        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.id} - {self.product_item.name} - {self.cost_price}"
