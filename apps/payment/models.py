from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from jalali_date import date2jalali

from apps.common.models import BaseModel
from apps.utils.validators import ValidateFileExtension
from apps.utils.date_convertor import jalali_to_gregorian

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
    other_info = models.JSONField(default=dict)

    @property
    def payment_date_jalali(self):
        return date2jalali(self.payment_date).strftime("%Y/%m/%d")

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} | {self.payment_date_jalali}"


class PaymentRequest(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_payment_request",
        verbose_name=_("user"),
    )
    paid_price = models.PositiveBigIntegerField(_("payment price"))
    paid_date = models.DateField(_("payment date"))
    is_confirmed = models.BooleanField(_("is confirmed"), default=False)

    @property
    def paid_date_jalali(self):
        return date2jalali(self.paid_date).strftime("%Y/%m/%d")

    @paid_date_jalali.setter
    def paid_date_jalali(self, value: str):
        self.paid_date = jalali_to_gregorian(value)

    def confirm(self):
        if not self.confirm:
            Payment.objects.create(
                user=self.user,
                payment_date=self.paid_date,
                payment_price=self.paid_price,
                payment_type="MA",
                other_info={"request_id": self.pk},
            )

    def undo_confirm(self):
        if self.confirm:
            Payment.objects.filter(other_info__request_id=self.pk).delete()

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} | {self.paid_date}"


class PaymentRequestAttachment(models.Model):
    EXTENSIONS = [".png", ".jpg", ".jpeg", ".pdf"]

    payment_request = models.ForeignKey(
        PaymentRequest,
        on_delete=models.CASCADE,
        related_name="payment_request_attachment",
        verbose_name=_("payment request"),
    )
    attachment = models.FileField(
        _("attachment"), validators=[ValidateFileExtension(EXTENSIONS)]
    )

    def __str__(self) -> str:
        return f"{self.payment_request.__str__} | {self.pk}"
