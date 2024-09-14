from django.shortcuts import render

from techcity.groups.models import Group


def index(request):
    context = {
        # TODO: upcoming events
        # TODO: recent events
        # TODO: hackathons
        "groups": Group.objects.all().order_by("name"),
    }
    return render(request, "core/index.html", context)
