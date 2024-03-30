from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from apps.payment import views

app_name = "payment"

router = DefaultRouter()
router.register(
    "payment-request", views.PaymentRequestUserVS, basename="payment-request"
)
router.register("payment-user", views.PaymentUserVS, basename="payment-user")
router.register("payment-admin", views.PaymentAdminVS, basename="payment-admin")

attachment_router = routers.NestedSimpleRouter(
    router, "payment-request", lookup="payment_request"
)
attachment_router.register(
    "attachment", views.PaymentRequestAttachmentVS, basename="attachment"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(attachment_router.urls)),
]
