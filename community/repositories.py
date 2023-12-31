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

    def create(self, group: Group, event_data: dict) -> Event:
        """Create an event and persist it."""
        event = Event(**event_data)

        group_events = self.events_path / group.slug
        group_events.mkdir(exist_ok=True)

        event_dict = event.model_dump()
        with open(group_events / f"{event.id}.yaml", "w") as f:
            f.write(yaml.dump(event_dict, sort_keys=True))

        return event
