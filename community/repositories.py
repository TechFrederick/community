"""A reposiory handles loading and accessing model data"""


import frontmatter
import markdown
import yaml

from .constants import data_path
from .extensions import TailwindExtension
from .models import Event, Group


class GroupRepository:
    def __init__(self):
        self._groups = self._load_groups()

    def _load_groups(self):
        groups = []
        groups_path = data_path / "groups"

        for filepath in sorted(groups_path.glob("*")):
            with open(filepath, "r") as f:
                metadata, description = frontmatter.parse(f.read())
            description = markdown.markdown(
                description,
                extensions=[TailwindExtension()],
            )
            metadata["description"] = description
            groups.append(Group(**metadata))

        return groups

    def all(self):
        return self._groups


class EventRepository:
    def __init__(self):
        self.events_path = data_path / "events"
        self.events_by_group = {}
        self.all_events = []
        self._load_events()

    def _load_events(self):
        """Scan the events directory to load the events in memory."""
        for dir in sorted(self.events_path.glob("*")):
            group_slug = dir.name
            group_events = []
            self.events_by_group[group_slug] = group_events
            for event_filename in sorted(dir.glob("*")):
                with open(event_filename, "r") as f:
                    event = Event(**yaml.safe_load(f))

                group_events.append(event)
                self.all_events.append(event)

            group_events.sort(key=lambda e: e.time, reverse=True)

        self.all_events.sort(key=lambda e: e.time, reverse=True)

    def create(self, group: Group, event_data: dict) -> Event:
        """Create an event and persist it."""
        event = Event(group_slug=group.slug, **event_data)

        group_events = self.events_path / group.slug
        group_events.mkdir(exist_ok=True)

        event_dict = event.model_dump()
        with open(group_events / f"{event.id}.yaml", "w") as f:
            f.write(yaml.dump(event_dict, sort_keys=True))

        return event
