from apps.common.managers import BaseManager
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class BaseUserManager(BaseManager, UserManager):
    def create_superuser(
        self,
        personal_code: str,
        firstname: str,
        lastname: str,
        phone_number: str,
        email: str,
        password=None,
        **extra_fields
    ):
        if not personal_code:
            raise ValueError(_("User must have a personal code"))
        if not password:
            raise ValueError(_("User must have a password"))
        if not firstname:
            raise ValueError(_("User must have a firstname"))
        if not lastname:
            raise ValueError(_("User must have a lastname"))
        if not phone_number:
            raise ValueError(_("User must have a mobile_phone"))
        if not email:
            raise ValueError(_("User must have a email"))

        user = self.model(email=self.normalize_email(email))
        user.firstname = firstname
        user.personal_code = personal_code
        user.lastname = lastname
        user.phone_number = phone_number
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
