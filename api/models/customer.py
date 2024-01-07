from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel, Business


class Customer(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.id}-{self.name}-{self.business.id}"
