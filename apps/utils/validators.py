import os
from typing import List

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

from django.utils.translation import gettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    regex = r"^(?:98|\+98|0098|0)?9[0-9]{9}$"
    message = _("mobile phone format is not valid")


@deconstructible
class ValidateFileExtension:
    def __init__(self, valid_extensions: List[str]) -> None:
        self.valid_extensions: List[str] = valid_extensions

    def __call__(self, value) -> None:
        self.validate(value)

    def validate(self, value):
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in self.valid_extensions:
            raise ValidationError(_("file format is not valid"))
