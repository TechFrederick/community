from django.urls import path

from .views import get_groups

app_name = "api"
urlpatterns = [
    path("v1/groups", get_groups),
]
