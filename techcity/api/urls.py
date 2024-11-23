from django.urls import path

from techcity.core.views import get_brand

from .views import get_groups

app_name = "api"
urlpatterns = [
    path("v1/brand", get_brand, name="brand"),
    path("v1/groups", get_groups, name="groups"),
]
