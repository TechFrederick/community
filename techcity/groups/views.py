from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from techcity.events.calendar import make_calendar
from techcity.events.models import Event

from .models import Group


def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    now = timezone.now()
    events = Event.objects.filter_around(now).filter(group=group).order_by("-start_at")
    context = {
        "group": group,
        "events": events,
        "now": now,
    }
    return render(request, "groups/detail.html", context)


def group_events(request, slug):
    group = get_object_or_404(Group, slug=slug)
    to_datetime = timezone.now() + timedelta(days=45)
    events = (
        Event.objects.filter_timeframe(to_datetime=to_datetime)
        .filter(group=group)
        .order_by("-start_at")
    )
    context = {
        "group": group,
        "events": events,
    }
    return render(request, "groups/events.html", context)


def group_ical(request, slug):
    group = get_object_or_404(Group, slug=slug)
    events = Event.objects.filter(group=group).order_by("-start_at")
    calendar = make_calendar(f"{group.name} Events", events)
    return HttpResponse(calendar.to_ical(), content_type="text/calendar")
