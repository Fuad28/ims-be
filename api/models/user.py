from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from api.enums import UserRoleEnum
from api.models import BusinessTimeAndUUIDStampedBaseModel

# from api.tasks.mail import send_email


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


null_blank = {"null": True, "blank": True}


class User(BusinessTimeAndUUIDStampedBaseModel, AbstractUser):
    username = None  # Email is primary user identifier, so username should be removed from defaults
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, **null_blank)
    role = models.CharField(
        max_length=11, choices=UserRoleEnum.choices, default=UserRoleEnum.ADMIN
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "business"]

    def __str__(self):
        return f"{self.id}-{self.full_name}-{self.email}"
