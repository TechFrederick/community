from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from techcity.events.models import Event

from .models import Group


def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    now = timezone.now()
    context = {
        "group": group,
        "events": Event.objects.filter_around(now).filter(group=group),
        "now": now,
    }
    return render(request, "groups/detail.html", context)


def group_events(request, slug):
    context = {
        "group": get_object_or_404(Group, slug=slug),
    }
    # TODO: use a different template
    return render(request, "groups/detail.html", context)
