# from django.urls import path
from django_distill import distill_path

from .views import index, up

app_name = "core"
urlpatterns = [
    distill_path(
        "", index, name="index", distill_func=lambda: None, distill_file="index.html"
    ),
    distill_path(
        "up", up, name="up", distill_func=lambda: None, distill_file="up.html"
    ),
]
