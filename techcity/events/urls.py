from django.urls import path

from .views import event_detail, events_ical

app_name = "events"
urlpatterns = [
    path("ical", events_ical, name="ical"),
    path("<str:sqid>", event_detail, name="detail"),
]
