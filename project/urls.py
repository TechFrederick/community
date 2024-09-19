from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("techcity.core.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("techcity.events.urls")),
    path("groups/", include("techcity.groups.urls")),
]
