from django.shortcuts import get_object_or_404, render
from django.utils import timezone

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
    context = {
        "group": group,
        "events": Event.objects.filter(group=group).order_by("-start_at"),
    }
    return render(request, "groups/events.html", context)
