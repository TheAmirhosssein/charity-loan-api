import re

import datetime
from django.core.exceptions import ValidationError
from jdatetime import date as Date
from typing import List


def jalali_to_gregorian(date: datetime.date | str) -> datetime.date:
    date = str(date)
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    if not re.match(date_pattern, date):
        raise ValidationError(
            f"Date has wrong format {date}: . Use one of these formats instead: YYYY-MM-DD."
        )
    else:
        splitted_date: list = [int(date) for date in date.split("-")]
        converted_date = Date(
            year=splitted_date[0], month=splitted_date[1], day=splitted_date[2]
        ).togregorian()
        return converted_date


def last_day_of_month(month: int) -> int:
    year = jalali_to_gregorian(datetime.date.today()).year
    date = Date(year=year, month=month, day=1)
    if month <= 6:
        return 31
    if (month == 12 and date.isleap()) or (month > 6):
        return 30
    else:
        return 29


def range_to_end_month(date: datetime.date | str) -> List[datetime.date]:
    splitted_date = date.split("-")
    month = splitted_date[1]
    month_last_day = last_day_of_month(int(month))
    start_date = jalali_to_gregorian(date)
    finish_date = jalali_to_gregorian(f"{splitted_date[0]}-{month}-{month_last_day}")
    return [start_date, finish_date]
