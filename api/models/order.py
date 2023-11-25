from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, ProductItem, Vendor

class Order(BusinessTimeAndUUIDStampedBaseModel):
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name= "orders")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name= "orders")
    placement_date = models.DateField()
    expected_receipt_date = models.DateField()
    actual_receipt_date = models.DateField(null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    qty_delayed = models.IntegerField()
    qty_defected = models.IntegerField()
    qty_accepted = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.product_item} from {self.vendor}- {self.business.id}"
