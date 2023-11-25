from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, ProductItem

class Vendor(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    qdp_rating = models.FloatField()

    @property
    def products(self) -> models.QuerySet[ProductItem]:
        return self.product_items.all()



    def __str__(self):
        return f"{self.id} - {self.name} - {self.qdp_rating}"
    

