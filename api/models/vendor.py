from django.db import models
from .business import Business

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    qdp_rating = models.FloatField()

    def __str__(self):
        return self.name
