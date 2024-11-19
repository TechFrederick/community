import bisect

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
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
        "upcoming_events": events[index:],
        "recent_events": reversed(events[:index]),
        "groups": Group.objects.all().order_by("name"),
    }
    return render(request, "core/index.html", context)


def manifest(request):
    # TODO: This should be made generic and not reference techfrederick directly.
    # Limits and details at
    # https://developer.chrome.com/docs/extensions/reference/manifest#minimal-manifest
    data = {
        "manifest_version": 3,
        "display": "standalone",
        "name": "techfrederick Community",  # max of 75
        "description": "Join tech-minded people from the Frederick area",  # max of 132
        "start_url": reverse("core:index"),
        "icons": [
            {"src": "/static/300x300.webp", "sizes": "192x192"},
            {"src": "/static/300x300.webp", "sizes": "512x512"},
        ],
        "background_color": "#1f92c9",  # A light blue
        "theme_color": "#143962",  # A dark blue
    }
    return JsonResponse(data)


def up(request):
    """A healthcheck to show when the app is up and able to respond to requests."""
    return render(request, "core/up.html", {})
