from django.urls import path, include

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
]
