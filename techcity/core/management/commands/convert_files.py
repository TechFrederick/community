from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

import frontmatter
import markdown
import yaml
from django.core.management.base import BaseCommand

from techcity.constants import data_path
from techcity.events.models import Event, Venue
from techcity.groups.models import Group

from . import static_models


class EventRepository:
    def __init__(self) -> None:
        self.events_path = data_path / "events"
        self.events_path.mkdir(exist_ok=True)

        self.events_by_time = defaultdict(set)  # For joint event detection
        self._load_events()

    def _load_events(self):
        """Scan the events directory to load the events in memory."""
        for dir in sorted(self.events_path.glob("*")):
            for event_filename in sorted(dir.glob("*")):
                with open(event_filename) as f:
                    event = static_models.Event(**yaml.load(f, Loader=yaml.Loader))  # noqa: S506

                self.events_by_time[event.start_at].add(event)

    def list(self) -> Iterable[static_models.Event]:
        """Get a list of events."""
        return self._all()

    def _all(self):
        for _, events in sorted(self.events_by_time.items()):
            yield from sorted(events, key=lambda e: e.id)


class GroupRepository:
    def __init__(self):
        self._groups_by_slug: dict[str, static_models.Group] = {}
        self._groups = self._load_groups()

    def _load_groups(self):
        groups = []
        groups_path = data_path / "groups"

        for filepath in sorted(groups_path.glob("*")):
            with open(filepath) as f:
                metadata, description = frontmatter.parse(f.read())
            description = markdown.markdown(description)
            metadata["description"] = description
            group = static_models.Group(**metadata)  # type: ignore
            groups.append(group)
            self._groups_by_slug[group.slug] = group

        return groups

    def all(self) -> list[static_models.Group]:
        return self._groups


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
            if group.extensions and group.extensions.meetup:
                defaults["event_source"] = Group.EventSource.MEETUP
                defaults["event_source_id"] = group.extensions.meetup.slug
            elif group.extensions and group.extensions.wordpress:
                defaults["event_source"] = Group.EventSource.WORDPRESS

            db_group, _ = Group.objects.update_or_create(
                slug=group.slug, defaults=defaults
            )
            groups[group.slug] = db_group

        event_repo = EventRepository()
        venues = {}
        for event in sorted(event_repo.list(), key=lambda e: e.start_at):
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

        for event in sorted(event_repo.list(), key=lambda e: e.start_at):
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
