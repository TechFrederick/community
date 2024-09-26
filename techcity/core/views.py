import bisect

from django.shortcuts import render
from django.utils import timezone

from techcity.events.models import Event, combine_joint_events
from techcity.groups.models import Group


def index(request):
    now = timezone.now()
    events = combine_joint_events(
        Event.objects.filter_around(now).select_related("group", "venue")
    )
    index = bisect.bisect_left(events, now, key=lambda e: e.start_at)
    context = {
        "now": now,
        "upcoming_events": reversed(events[index:]),
        "recent_events": reversed(events[:index]),
        "groups": Group.objects.all().order_by("name"),
    }
    return render(request, "core/index.html", context)


def up(request):
    """A healthcheck to show when the app is up and able to respond to requests."""
    return render(request, "core/up.html", {})
