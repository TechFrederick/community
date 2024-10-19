from datetime import timedelta

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .calendar import make_calendar
from .models import Event, combine_joint_events


def event_detail(request, sqid):
    try:
        event = Event.objects.from_sqid(sqid)
    except Event.DoesNotExist:
        return HttpResponseNotFound()
    context = {"event": event}
    return render(request, "events/detail.html", context)


def events_ical(request):
    now = timezone.now()
    from_datetime = now - timedelta(days=90)
    to_datetime = now + timedelta(days=30)
    events = combine_joint_events(
        Event.objects.filter_timeframe(from_datetime, to_datetime)
    )
    calendar = make_calendar("techfrederick Community Events", events)
    return HttpResponse(calendar.to_ical())  # , content_type="text/calendar")
