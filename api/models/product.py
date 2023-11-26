from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, Vendor, Category, SizeCategory
from api.utils.utils import generate_serial_number

null_blank= {"null": True, "blank": True}
class Product(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    image = models.URLField(**null_blank)

    @property
    def quantity(self):
        self.product_items.aggregate(total_sum= models.Sum("quantity"))["total_sum"]

    def __str__(self):
        return f"{self.id} - {self.name} - {self.quantity}"


class ProductItem(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= "product_items")
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, related_name= "product_items", **null_blank)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name= "product_items", **null_blank)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name= "product_items", **null_blank)
    serial_no= models.CharField(max_length= 10)
    quantity = models.IntegerField(default=0)
    safety_stock = models.IntegerField(default=0)
    reordering_point = models.IntegerField(default=0)
    lead_time = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    ordering_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    expiring_date = models.DateField(**null_blank)
    barcode = models.CharField(max_length=255)
    image = models.URLField(**null_blank)
    

    def save(self, *args, **kwargs) -> None:
        if not self.serial_no:
            count= ProductItem.objects.filter(business= self.business).count()
            self.serial_no= generate_serial_number(count)

        if not self.name:
            self.name= f"{self.product.name} ({self.size_category.name})"

        return super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.id} - {self.product.name} - {self.size_category.name}"
