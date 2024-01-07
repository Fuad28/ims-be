from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel


class SizeCategory(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Category(BusinessTimeAndUUIDStampedBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"
