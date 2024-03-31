from apps.common.managers import BaseManager

from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentManagers(BaseManager):
    def automatic_payment(self, *args, **kwargs):
        users = User.objects.filter(*args, **kwargs)
        for user in users:
            self.create(
                payment_price=user.monthly_payment,
                user=user,
                payment_type="AM",
            )
