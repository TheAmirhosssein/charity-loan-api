from django.contrib import admin

from apps.payment import models
from apps.common.admin import BaseModelAdmin


class UserAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "payment_price",
        "payment_date",
        "payment_type",
        "user",
    )

    search_fields = "payment_date"


admin.site.register(models.Payment)
