from django.db import models, transaction
from api.models import ProductItem, Customer, BusinessTimeAndUUIDStampedBaseModel

class Sale(BusinessTimeAndUUIDStampedBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name= "sales")
    description = models.CharField(max_length= 255, null= True, blank= True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0)

    @property
    def sale_items(self):
        return self.sale_items.all()

    
    def __str__(self):
        return f"{self.id} - {self.created_at} - {self.customer.name}"
    

class SaleItem(BusinessTimeAndUUIDStampedBaseModel):
    sale= models.ForeignKey(Sale, on_delete= models.CASCADE, related_name= "sale_items")
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name= "sales")
    quantity = models.IntegerField()
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_item.quantity -= self.quantity
            self.product_item.save()
            

        new_selling_price = self.quantity * self.unit_selling_price
        if new_selling_price != self.selling_price:
            self.sale.total_selling_price += new_selling_price - self.selling_price
            self.selling_price= new_selling_price
            self.sale.save()

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.id} - {self.sale.id} - {self.product_item.name}"
