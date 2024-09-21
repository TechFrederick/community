from django.core.management.base import BaseCommand

from techcity.events.models import Event, Venue
from techcity.groups.models import Group
from techcity.models import EventListFilterOptions
from techcity.services.events.repository import EventRepository
from techcity.services.groups.repository import GroupRepository


def clean_address(address):
    """Clean the address.

    Some of the addresses that come from Meetup are trash. Since address is
    the unique key, it needs to be cleaned up to make sure that we match
    places that should be equal.
    """
    return address.strip().rstrip(",")


class Command(BaseCommand):
    help = "Converts the existing data files for the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Converting data files to database entries...")
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
        venues = {}
        for event in sorted(
            event_repo.list(EventListFilterOptions()), key=lambda e: e.start_at
        ):
            if event.venue:
                cleaned_address = clean_address(event.venue.address)
                if cleaned_address not in venues:
                    print(f"Venue {cleaned_address}...")
                    defaults = {
                        "city": event.venue.city.strip(),
                        "state": event.venue.state,
                        "zip": event.venue.zip,
                        "lat": event.venue.lat,
                        "long": event.venue.lon,
                    }
                    venues[cleaned_address], _ = Venue.objects.update_or_create(
                        address=cleaned_address, defaults=defaults
                    )

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
            }
            if event.venue:
                cleaned_address = clean_address(event.venue.address)
                defaults["venue"] = venues.get(cleaned_address)

            Event.objects.update_or_create(url=event.link, defaults=defaults)
