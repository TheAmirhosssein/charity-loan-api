from datetime import datetime

from jalali_date import date2jalali

from apps.payment.models import Payment


def automatic_payment():
    jalali_date = date2jalali(datetime.today())
    if jalali_date.day == 1:
        Payment.objects.automatic_payment(is_admin=False)
