from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payment import views

app_name = "payment"

router = DefaultRouter()
router.register(
    "payment-request-user", views.PaymentRequestUser, basename="payment-request-user"
)

urlpatterns = [
    path("", include(router.urls)),
]
