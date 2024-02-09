from django.urls import path
from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("user/create/", views.CreateUserAV.as_view(), name="create_user"),
]
