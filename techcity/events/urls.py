# from django.urls import path
from django_distill import distill_path

from .views import event_detail
from .models import Event


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
