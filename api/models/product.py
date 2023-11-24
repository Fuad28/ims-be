from django.db import models
from .vendor import Vendor 
from .business import Business


class Product(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    delayed = models.IntegerField()
    defected = models.IntegerField()
    accepted = models.IntegerField()
    expiring_date = models.DateField()
    comment = models.TextField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    quantity = models.IntegerField(default=0)


class ProductSizeCategory(models.Model):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class ProductItem(models.Model):
    size_category = models.ForeignKey('ProductSizeCategory', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    ordering_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    safety_stock = models.IntegerField(default=0)
    expiring_date = models.DateField()
    barcode = models.CharField(max_length=255)
    image = models.URLField()



class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
