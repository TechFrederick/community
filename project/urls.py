from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("", include("techcity.core.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("techcity.events.urls")),
    path("groups/", include("techcity.groups.urls")),
    path("api/", include("techcity.api.urls")),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]

# Enable the debug toolbar only in DEBUG mode.
if settings.DEBUG and settings.DEBUG_TOOLBAR:
    urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
