from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    regex = r"^(?:98|\+98|0098|0)?9[0-9]{9}$"
    message = _("mobile phone format is not valid")
