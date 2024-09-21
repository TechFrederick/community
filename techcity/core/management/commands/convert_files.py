from django.core.management.base import BaseCommand

from techcity.events.models import Event
from techcity.groups.models import Group
from techcity.models import EventListFilterOptions
from techcity.services.events.repository import EventRepository
from techcity.services.groups.repository import GroupRepository


class Command(BaseCommand):
    help = "Converts the existing data files for the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Converting data files to database entries...")
        # TODO: process venues
        # TODO: pull meetup info about groups and events
        # TODO: pull wordpress info out of techfrederick group
        group_repo = GroupRepository()
        groups = {}
        for group in sorted(group_repo.all(), key=lambda g: g.slug):
            print(f"Updating {group.name}...")
            defaults = {
                "name": group.name,
                "url": group.url,
                "description": group.description,
                "teaser": group.teaser,
                "color": group.color,
            }
            db_group, _ = Group.objects.update_or_create(
                slug=group.slug, defaults=defaults
            )
            groups[group.slug] = db_group

        event_repo = EventRepository()
        for event in sorted(
            event_repo.list(EventListFilterOptions()), key=lambda e: e.start_at
        ):
            print(f"Event {event.name}...")
            defaults = {
                "name": event.name,
                "group": groups[event.group_slug],
                "start_at": event.start_at,
                "end_at": event.end_at,
                "description": event.description,
                # TODO: link to venue
            }
            Event.objects.update_or_create(url=event.link, defaults=defaults)
