# from django.urls import path
from django_distill import distill_path

from .models import Event
from .views import event_detail


def get_all_events():
    for event in Event.objects.all():
        yield {"sqid": event.sqid}


app_name = "events"
urlpatterns = [
    distill_path(
        "<str:sqid>.html",
        event_detail,
        name="detail",
        distill_func=get_all_events,
        distill_file="events/{sqid}.html",
    ),
]
