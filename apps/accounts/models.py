import os
import random
import string
from datetime import timedelta

from apps.common.models import BaseModel
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_resized import ResizedImageField
from django.utils import timezone

from apps.accounts.managers import BaseUserManager


def create_expired_time():
    return timezone.now() + timedelta(minutes=10)


def create_refresh_time():
    return timezone.now() + timedelta(minutes=2)


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(_("images format is not valid"))


class PhoneNumberValidator(RegexValidator):
    regex = r"^(?:98|\+98|0098|0)?9[0-9]{9}$"
    message = _("mobile phone format is not valid")


class User(BaseModel, AbstractUser, PermissionsMixin):
    GENDERS = [
        ("M", _("male")),
        ("F", _("female")),
    ]

    username = models.CharField(
        _("username"),
        max_length=50,
        null=True,
        unique=False,
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        unique=True,
        validators=[PhoneNumberValidator()],
        error_messages={"unique": _("phone number is duplicated")},
    )
    avatar = ResizedImageField(
        _("avatar"),
        null=True,
        blank=True,
        size=[200, 200],
        crop=["middle", "center"],
        quality=99,
        upload_to="avatar",
        validators=[validate_image_extension],
        max_length=500,
    )
    personal_code = models.CharField(
        _("personal code"),
        max_length=20,
        unique=True,
        error_messages={"unique": _("personal code is duplicated")},
    )
    email = models.EmailField(_("email"), null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=10, choices=GENDERS)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    objects = BaseUserManager()

    USERNAME_FIELD = "personal_code"
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
    ]

    def __str__(self) -> str:
        if self.last_name is None and self.first_name is None:
            return self.username
        return self.get_full_name()


class OTPRequest(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
    )
    otp = models.CharField(max_length=6, default=generate_otp)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField(default=create_expired_time)
    refresh = models.DateTimeField(default=create_refresh_time)

    def is_expired(self):
        refresh = self.created + timedelta(minutes=2)
        if refresh < timezone.now():
            return True
        return False

    def is_refresh(self):
        refresh = self.created + timedelta(minutes=2)
        if refresh < timezone.now():
            return False
        return True

    def __str__(self) -> str:
        return f"{self.user.username}"
