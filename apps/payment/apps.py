from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payment"

    def ready(self) -> None:
        from apps.payment.scheduler import start

        start()
        return super().ready()
