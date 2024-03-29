from typing import Any

from django.db import models
from django.http import Http404
from django.utils import timezone


class BaseManager(models.Manager):
    def filter(self, *args: Any, **kwargs: Any):
        return super().filter(
            deleted=False,
            *args,
            **kwargs,
        )

    def get(self, *args: Any, **kwargs: Any) -> Any:
        return super().get(deleted=False, *args, **kwargs)

    def all(self):
        return super().all().exclude(deleted=True)

    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True)

    def delete(self):
        self.update(deleted=True, deleted_at=timezone.now())

    def get_object_or_admin_or_404(self, user, field: str, *args, **kwargs):
        if user.is_admin_user:
            del kwargs[field]
        try:
            return self.get(*args, **kwargs)
        except Exception:
            raise Http404()

    def get_list_or_admin_or_404(self, user, field: str, *args, **kwargs):
        if user.is_admin_user:
            del kwargs[field]
        try:
            return self.filter(*args, **kwargs)
        except Exception:
            raise Http404()
