from django.urls import path

from .views import group_detail, group_events

app_name = "groups"
urlpatterns = [
    path("<slug:slug>", group_detail, name="detail"),
    path("<slug:slug>/events", group_events, name="events"),
]
