from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts import views

app_name = "accounts"

router = DefaultRouter()
router.register("", views.UserAdminVS, basename="user_admin")

urlpatterns = [
    path("user/", include(router.urls), name="create_user"),
]
