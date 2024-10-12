from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Event


def event_detail(request, sqid):
    try:
        event = Event.objects.from_sqid(sqid)
    except Event.DoesNotExist:
        return HttpResponseNotFound()
    context = {"event": event}
    return render(request, "events/detail.html", context)
