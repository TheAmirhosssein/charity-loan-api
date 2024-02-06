from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "personal_code",
        "first_name",
        "last_name",
    )
    readonly_fields = ("last_login",)

    search_fields = ("phone_number", "lastname", "firstname")
    ordering = ("-id",)
    filter_horizontal = ("user_permissions", "groups")


admin.site.register(User, UserAdmin)
