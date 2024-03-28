from django.db import models
from apps.common.managers import BaseManager
from django.utils import timezone
from jalali_date import datetime2jalali


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, editable=False)

    objects = BaseManager()

    SOFT_DELETE = True

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def delete(self) -> tuple[int, dict[str, int]] | None:
        if self.SOFT_DELETE:
            self.deleted = True
            self.deleted_at = timezone.now()
            self.save()
        else:
            return super().delete()

    @property
    def created_at_jalali(self):
        return datetime2jalali(self.created_at).strftime("%Y/%m/%d - %H:%M:%S")

    @property
    def updated_at_jalali(self):
        return datetime2jalali(self.updated_at).strftime("%Y/%m/%d - %H:%M:%S")
