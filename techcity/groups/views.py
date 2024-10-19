from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from icalendar import Calendar
from icalendar import Event as CalendarEvent

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
    calendar = Calendar()
    calendar.add("prodid", "-//techfrederick Community//Community Website//EN")
    calendar.add("version", "2.0")
    calendar.add("x-wr-calname", f"{group.name} Events")

    for event in Event.objects.filter(group=group).order_by("-start_at"):
        calendar_event = CalendarEvent()
        calendar_event.add("summary", event.name)
        calendar_event.add("uid", event.id)
        # FIXME: We don't currently track a created or last modified datetime
        # on an event, but dtstamp is required. Use the start time has a stand-in.
        # The impact of this is that calendar clients won't really update an event
        # unless the start time changes, which isn't great.
        calendar_event.add("dtstamp", event.start_at)
        calendar_event.start = event.start_at
        calendar_event.end = event.end_at
        calendar.add_component(calendar_event)

    return HttpResponse(calendar.to_ical(), content_type="text/calendar")
