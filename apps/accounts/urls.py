from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts import views

app_name = "accounts"

router = DefaultRouter()
router.register("user", views.UserAdminVS, basename="user_admin")

urlpatterns = [
    path("", include(router.urls), name="create_user"),
    path("send-otp/", views.SendOTP.as_view(), name="send_otp"),
    path("verify-otp/", views.VerifyOTP.as_view(), name="verify_otp"),
    path("edit-profile/", views.EditUserInfoAV.as_view(), name="edit_info"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
