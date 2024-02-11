from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts import views

app_name = "accounts"

router = DefaultRouter()
router.register("user", views.UserAdminVS, basename="user_admin")

urlpatterns = [
    path("", include(router.urls), name="create_user"),
    path("send-otp/", views.SendOTP.as_view(), name="send_otp"),
]
