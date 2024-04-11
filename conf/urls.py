from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = []


if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.api.urls")),
)
