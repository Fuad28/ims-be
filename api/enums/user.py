from django.db.models import TextChoices


class UserRoleEnum(TextChoices):
    ADMIN = "admin"
    STORE_CLERK = "store_clerk"
