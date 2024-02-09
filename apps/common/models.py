import uuid

from django.db import models
from apps.common.managers import BaseManager
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, editable=False)
    uuid = models.CharField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=36
    )

    objects = BaseManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
