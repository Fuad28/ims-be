from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, Vendor
from api.utils.utils import generate_serial_number


class Product(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    image = models.URLField()

    @property
    def quantity(self):
        self.product_items.aggregate(total_sum= models.Sum("quantity"))["total_sum"]

    def __str__(self):
        return f"{self.id} - {self.name} - {self.quantity}"


class ProductSizeCategory(BusinessTimeAndUUIDStampedBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= "product_sizes")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.product.name} - {self.name}"



class ProductCategory(BusinessTimeAndUUIDStampedBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= "product_categories")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.product.name} - {self.name}"
    


class ProductItem(BusinessTimeAndUUIDStampedBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= "product_items")
    size_category = models.ForeignKey(ProductSizeCategory, on_delete=models.CASCADE, related_name= "product_items")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name= "product_items")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name= "product_items")
    serial_no= models.CharField(max_length= 10)
    quantity = models.IntegerField(default=0)
    safety_stock = models.IntegerField(default=0)
    reordering_point = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    ordering_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    expiring_date = models.DateField()
    barcode = models.CharField(max_length=255)
    image = models.URLField()
    

    def save(self, *args, **kwargs) -> None:
        if not self.serial_no:
            count= self.objects.filter(business= self.business).count()
            self.serial_no= generate_serial_number(count)

        return super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.id} - {self.product.name} - {self.size_category.name}"
