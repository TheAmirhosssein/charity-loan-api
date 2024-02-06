import uuid

from django.db import models
from apps.common.managers import BaseManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    uuid = models.CharField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=36
    )

    objects = BaseManager()

    class Meta:
        abstract = True
