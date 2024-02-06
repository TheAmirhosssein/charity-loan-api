from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
