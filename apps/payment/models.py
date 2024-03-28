from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from jalali_date import date2jalali

from apps.common.models import BaseModel

User = get_user_model()


class Payment(BaseModel):
    TYPES = [("AM", _("automatic")), ("MA", _("manually"))]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_payment",
        verbose_name=_("user"),
    )
    payment_price = models.PositiveBigIntegerField(_("payment price"))
    payment_date = models.DateField(_("payment date"), default=timezone.now)
    payment_type = models.CharField(_("payment type"), choices=TYPES, max_length=5)
    is_valid = models.BooleanField(_("is valid"), default=True)

    @property
    def payment_date_jalali(self):
        return date2jalali(self.date_joined).strftime("%Y/%m/%d")

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} | {self.payment_date_jalali}"
