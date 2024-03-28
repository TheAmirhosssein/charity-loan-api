import os
import random
import string
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.accounts.managers import BaseUserManager
from apps.common.models import BaseModel
from apps.utils.validators import PhoneNumberValidator

OTP_EXPIRED_TIME = 1


def create_expired_time():
    return timezone.now() + timedelta(minutes=OTP_EXPIRED_TIME)


def create_refresh_time():
    return timezone.now() + timedelta(minutes=OTP_EXPIRED_TIME)


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(_("images format is not valid"))


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
    is_admin = models.BooleanField(_("is admin"), default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "personal_code"
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
    ]
    SOFT_DELETE = False

    def __str__(self) -> str:
        if self.last_name is None and self.first_name is None:
            return self.personal_code
        return self.get_full_name()

    def can_create_otp(self) -> bool:
        last_otp = (
            OTPRequest.objects.filter(user=self)
            .order_by(
                "created_at",
            )
            .last()
        )
        if last_otp is None:
            return True
        elif last_otp.is_expired():
            return True
        else:
            return False


class OTPRequest(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
    )
    otp = models.CharField(max_length=6, default=generate_otp)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField(default=create_expired_time)
    refresh = models.DateTimeField(default=create_refresh_time)
    uuid = models.UUIDField(
        primary_key=True,
        max_length=40,
        default=uuid.uuid4,
        unique=True,
    )
    verified_datetime = models.DateTimeField(null=True)

    SOFT_DELETE = False

    def is_expired(self) -> bool:
        if self.expired < timezone.now():
            return True
        return False

    def is_refresh(self) -> bool:
        if self.refresh < timezone.now():
            return False
        return True

    def verify_otp(self) -> None:
        self.verified = True
        self.verified_datetime = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f"{self.user}"


class SentSMS(BaseModel):
    REASONS = [("OTP", _("send otp code"))]
    REASONS = [("CM", _("custom message"))]

    phone_number = models.CharField(_("phone number"), max_length=50)
    text = models.TextField()
    reason = models.CharField(_("reason"), max_length=50, choices=REASONS)

    def __str__(self) -> str:
        return self.phone_number

    def get_user(self) -> User | None:
        user = User.objects.filter(phone_number=self.phone_number).first()
        return user
