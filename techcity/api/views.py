from django.http import JsonResponse

from ..groups.models import Group


def get_groups(request):
    group_objects = Group.objects.all()
    return JsonResponse(list(group_objects.values()), safe=False)
