from django.db import models
from .product import ProductItem
from .customer import Customer

class Sales(models.Model):
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    placement_date = models.DateField()
    expected_receipt_date = models.DateField()
    actual_receipt_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calculate total_price based on quantity and product selling_price
        if self.product and self.product.selling_price:
            self.amount = self.quantity * self.product.selling_price
        super().save(*args, **kwargs)
