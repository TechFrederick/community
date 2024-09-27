from django_distill import distill_path

from .views import group_detail, group_events

def get_all_groups():
    from .models import Group

    for group in Group.objects.all():
        yield {"slug": group.slug}

app_name = "groups"
urlpatterns = [
    distill_path("<slug:slug>", group_detail, name="detail", distill_func=get_all_groups, distill_file="groups/{slug}/index.html"),
    distill_path("<slug:slug>/events", group_events, name="events", distill_func=get_all_groups, distill_file="groups/{slug}/events.html"),
]
