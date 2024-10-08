from django.urls import path

from .views import event_detail

app_name = "events"
urlpatterns = [
    path("<str:sqid>", event_detail, name="detail"),
]
