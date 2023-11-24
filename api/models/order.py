from django.db import models
from .product import ProductItem
from .vendor import Vendor

class Order(models.Model):
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    placement_date = models.DateField()
    expected_receipt_date = models.DateField()
    actual_receipt_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.pk} - {self.product} from {self.vendor}"
