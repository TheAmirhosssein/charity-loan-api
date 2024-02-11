from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest


class BaseModelAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        return obj.delete()

    def delete_queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Any],
    ) -> None:
        return super().delete_queryset(request, queryset)
