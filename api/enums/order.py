from django.db.models import TextChoices


class OrderStatusEnum(TextChoices):
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED= "cancelled"
