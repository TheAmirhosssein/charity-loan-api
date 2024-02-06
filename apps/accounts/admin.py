from django.contrib import admin

from .models import User
from apps.common.admin import BaseModelAdmin


class UserAdmin(BaseModelAdmin):
    list_display = (
        "personal_code",
        "first_name",
        "last_name",
    )
    readonly_fields = ("last_login",)

    search_fields = ("phone_number", "lastname", "firstname")
    filter_horizontal = ("user_permissions", "groups")


admin.site.register(User, UserAdmin)
