from django.shortcuts import get_object_or_404, render

from .models import Group


def group_detail(request, slug):
    context = {
        "group": get_object_or_404(Group, slug=slug),
        # TODO: need `events` in context.
    }
    return render(request, "groups/detail.html", context)


def group_events(request, slug):
    context = {
        "group": get_object_or_404(Group, slug=slug),
    }
    # TODO: use a different template
    return render(request, "groups/detail.html", context)
