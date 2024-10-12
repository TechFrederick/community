from django.urls import path

from .views import index, up

app_name = "core"
urlpatterns = [
    path("", index, name="index"),
    path("up", up, name="up"),
]
