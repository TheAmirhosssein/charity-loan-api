from typing import Any

from django.db import models


class BaseManager(models.Manager):
    def filter(self, *args: Any, **kwargs: Any):
        return super().filter(*args, **kwargs).exclude(deleted=True)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        return super().get(*args, **kwargs).exclude(deleted=True)

    def all(self):
        return super().all().exclude(deleted=True)
