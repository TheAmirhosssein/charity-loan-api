from typing import Any

from django.db import models
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

    def all_admin_filtered_users(self, user, *args, **kwargs):
        if not user.is_authenticated:
            return self.none()
        if user.is_admin_user:
            return self.all()
        else:
            return self.filter(*args, **kwargs)
