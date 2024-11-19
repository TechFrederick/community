from django.urls import path

from .views import index, manifest, up

app_name = "core"
urlpatterns = [
    path("", index, name="index"),
    path("manifest.json", manifest, name="manifest"),
    path("up", up, name="up"),
]
