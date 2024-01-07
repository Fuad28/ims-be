from django.db import models

from api.models import BusinessTimeAndUUIDStampedBaseModel
from api.enums import UserRoleEnum


class TeamInvitation(BusinessTimeAndUUIDStampedBaseModel):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=11, choices=UserRoleEnum.choices, default=UserRoleEnum.STORE_CLERK
    )
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}-{self.email}-{self.business.id}-{self.is_registered}"
