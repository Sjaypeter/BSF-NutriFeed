from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "farm_name", "is_verified", "date_joined"]
    list_filter = ["role", "is_verified", "is_staff"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("BSF-Nutrifeed Profile", {
            "fields": ("role", "phone_number", "farm_name", "farm_location", "is_verified")
        }),
    )