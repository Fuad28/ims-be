from django.db.models import TextChoices


class ProductItemStatusEnum(TextChoices):
    REORDER = "reorder"
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
