from django.urls import path, include

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("payment/", include("apps.payment.urls")),
]
