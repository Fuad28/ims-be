from django.db import models
from math import ceil
from api.models import BusinessTimeAndUUIDStampedBaseModel


class Vendor(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    qdp_rating = models.FloatField(default=0)
    lead_time = models.IntegerField(default=0)
    total_qdp_rating = models.FloatField(default=0)
    completed_orders = models.IntegerField(default=0)
    total_lead_time = models.IntegerField(default=0)

    @property
    def avg_lead_time(self):
        return ceil(self.total_lead_time / self.completed_orders)

    @property
    def avg_qdp_rating(self):
        return ceil(self.total_qdp_rating / self.completed_orders)

    @property
    def products(self) -> models.QuerySet:
        return self.product_items.all()

    def __str__(self):
        return f"{self.id} - {self.name} - {self.qdp_rating}"
