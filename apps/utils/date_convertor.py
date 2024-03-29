import re

import datetime
from django.core.exceptions import ValidationError
from jdatetime import date as Date


def jalali_to_gregorian(date: datetime.date) -> str:
    date = str(date)
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    if not re.match(date_pattern, date):
        raise ValidationError(
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
        )
    else:
        splitted_date: list = [int(date) for date in date.split("-")]
        converted_date = Date(
            year=splitted_date[0], month=splitted_date[1], day=splitted_date[2]
        ).togregorian()
        return converted_date
