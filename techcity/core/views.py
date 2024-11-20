import bisect

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from techcity.core.models import Brand
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
    brand = Brand.objects.active()
    # Details at
    # https://developer.chrome.com/docs/extensions/reference/manifest#minimal-manifest
    data = {
        "manifest_version": 3,
        "display": "standalone",
        "name": brand.name,
        "description": brand.tagline,
        "start_url": reverse("core:index"),
        "icons": [
            {"src": brand.icon_192x192_url, "sizes": "192x192"},
            {"src": brand.icon_512x512_url, "sizes": "512x512"},
        ],
        "background_color": "#1f92c9",  # A light blue
        "theme_color": "#143962",  # A dark blue
    }
    return JsonResponse(data)


def up(request):
    """A healthcheck to show when the app is up and able to respond to requests."""
    return render(request, "core/up.html", {})
