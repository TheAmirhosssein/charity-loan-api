import datetime
import random
from typing import List

from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
from jalali_date import date2jalali

from apps.accounts import models
from apps.common.managers import BaseManager
from apps.utils.date import range_to_end_month


class BaseUserManager(BaseManager, UserManager):
    def create_superuser(
        self,
        personal_code: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        password=None,
        **extra_fields,
    ):
        if not personal_code:
            raise ValueError(_("User must have a personal code"))
        if not password:
            raise ValueError(_("User must have a password"))
        if not first_name:
            raise ValueError(_("User must have a firstname"))
        if not last_name:
            raise ValueError(_("User must have a lastname"))
        if not phone_number:
            raise ValueError(_("User must have a mobile_phone"))
        if not email:
            raise ValueError(_("User must have a email"))

        user = self.model(email=self.normalize_email(email))
        user.firstname = first_name
        user.personal_code = personal_code
        user.lastname = last_name
        user.phone_number = phone_number
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def lottery(self, count: int, duplicate: bool = False, *args, **kwargs) -> List:
        users = (
            models.Winners.objects.available_users(*args, **kwargs)
            if not duplicate
            else list(self.filter(*args, **kwargs))
        )
        if count > len(users) or count <= 0:
            raise ValueError(
                _(
                    f"Given count is larger than users population or bellow 1. Max population is: {len(users)}"
                )
            )
        winners = random.sample(users, count)
        [models.Winners.objects.create(user_id=user.pk) for user in winners]
        winners_object = self.filter(pk__in=[user.pk for user in winners])
        return winners_object


class WinnersManager(BaseUserManager):
    def available_users(self, *args, **kwargs) -> List:
        current_date = str(date2jalali(datetime.date.today())).split("-")
        month_range = range_to_end_month(f"{current_date[0]}-{current_date[1]}-01")
        old_winners = self.filter(
            created_at__date__range=[month_range[0], month_range[1]],
        )
        users = list(
            models.User.objects.filter(*args, **kwargs).exclude(
                id__in=[old_winners.values_list("user_id")]
            )
        )
        return users
