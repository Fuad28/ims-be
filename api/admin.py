from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.user import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "full_name", "role", "business", "is_active", "is_staff", "created_at")
    list_filter = ("email", "full_name", "role", "business", "is_active", "is_staff", "created_at")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email", "full_name", "role", "business", "is_active", "is_staff", "created_at")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)

class BaseModelMixinAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


for model in apps.get_app_config("api").get_models():
    if (model != User):
        admin.site.register(model, admin.ModelAdmin)
