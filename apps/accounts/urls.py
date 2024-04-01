from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts import views

app_name = "accounts"

router = DefaultRouter()
router.register("user", views.UserAdminVS, basename="user_admin")
router.register("log", views.UserLogVS, basename="user_log")
router.register("sent-sms", views.SMSReportVS, basename="sent_sms")
router.register("winner", views.WinnersVS, basename="winner")

urlpatterns = [
    path("", include(router.urls)),
    path("send-otp/", views.SendOTP.as_view(), name="send_otp"),
    path("verify-otp/", views.VerifyOTP.as_view(), name="verify_otp"),
    path("profile/", views.EditUserInfoAV.as_view(), name="profile"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("send-sms/", views.SendSMSAV.as_view(), name="send_sms"),
    path("lottery/", views.Lottery.as_view(), name="lottery"),
]
