from django.db import models
from apps.common.managers import BaseManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
