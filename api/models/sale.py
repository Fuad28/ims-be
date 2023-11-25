from django.db import models
from api.models import ProductItem, Customer, BusinessTimeAndUUIDStampedBaseModel

class Sale(BusinessTimeAndUUIDStampedBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name= "sales")
    description = models.CharField(max_length= 255, null= True, blank= True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0)


    def save(self, *args, **kwargs):
        self.total_selling_price = self.sale_items.aggregrate(total_sp=  models.Sum("selling_price"))["total_sp"]

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id} - {self.created_at} - {self.customer.name}"
    

class SaleItem(BusinessTimeAndUUIDStampedBaseModel):
    sale= models.ForeignKey(Sale, on_delete= models.CASCADE, related_name= "sale_items")
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name= "sales")
    quantity = models.IntegerField(default= 1)
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.selling_price = self.quantity * self.unit_selling_price

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.id} - {self.sale.id} - {self.product_item.name}"
