"""A reposiory handles loading and accessing model data"""


from datetime import datetime, timedelta
import frontmatter
import markdown
import yaml
from collections import defaultdict
from typing import DefaultDict

from .constants import data_path
from .extensions import TailwindExtension
from .models import Event, Group


class GroupRepository:
    def __init__(self):
        self._groups_by_slug: dict[str, Group] = {}
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
            group = Group(**metadata)
            groups.append(group)
            self._groups_by_slug[group.slug] = group

        return groups

    def all(self) -> list[Group]:
        return self._groups

    def find_by(self, slug: str) -> Group:
        """Find a group from its slug name.

        Invalid slugs are designed to fail so that bad data gets corrected.
        """
        return self._groups_by_slug[slug]


class EventRepository:
    def __init__(self):
        self.events_path = data_path / "events"

        # Indices
        self.events_by_id: dict[str, Event] = {}
        self.events_by_group: DefaultDict[str, set[Event]] = defaultdict(set)
        self.events_by_time = defaultdict(set)  # For joint event detection

        self._load_events()

    def _load_events(self):
        """Scan the events directory to load the events in memory."""
        for dir in sorted(self.events_path.glob("*")):
            group_slug = dir.name
            for event_filename in sorted(dir.glob("*")):
                with open(event_filename, "r") as f:
                    event = Event(**yaml.safe_load(f))

                self.events_by_id[event.id] = event
                self.events_by_group[group_slug].add(event)
                self.events_by_time[event.time].add(event)

    def create(self, group: Group, event_data: dict) -> Event:
        """Create an event and persist it."""
        event = Event(group_slug=group.slug, **event_data)

        group_events = self.events_path / group.slug
        group_events.mkdir(exist_ok=True)

        self._update_indices(group, event)
        self._check_joint_events(event)
        self._save(group_events, event)
        return event

    def _update_indices(self, group, event):
        """Update the indices of the repository.

        If this is not updated, then weird conditions can happen with other checking
        (e.g., adding multiple new events at once may have a mismatched `joint_with` set).
        """
        old_event = self.events_by_id[event.id]
        self.events_by_id[event.id] = event

        self.events_by_group[group.slug].add(event)
        # There is a case where the event can change time and needs to move
        # to a different time set. Thus, we need to remove before adding,
        # which may look weird, but it's actually important.
        self.events_by_time[old_event.time].remove(old_event)
        self.events_by_time[event.time].add(event)

    def _check_joint_events(self, event):
        """Check if the event is a joint event with other groups.

        When a joint event is found, update linkages.
        """
        events = self.events_by_time[event.time]
        if len(events) <= 1:
            return

        # A joint event occurs when the two events are equal, but have different identities.
        joint_events = [event]
        for same_time_event in events:
            if event.id != same_time_event.id and event == same_time_event:
                joint_events.append(same_time_event)

        # No joint events detected. Bail out.
        if len(joint_events) == 1:
            return

        joint_with = [event.id for event in sorted(joint_events, key=lambda e: e.id)]
        # Update the joint events only if the full joint_with doesn't match.
        # Events exclude themselves from that list!
        for joint_event in joint_events:
            joint_ids = joint_with.copy()
            joint_ids.remove(joint_event.id)
            if set(joint_event.joint_with) != set(joint_with):
                joint_event.joint_with = joint_ids
                self._save(self.events_path / joint_event.group_slug, joint_event)

    def _save(self, outpath, event):
        event_dict = event.model_dump()
        with open(outpath / f"{event.id}.yaml", "w") as f:
            f.write(yaml.dump(event_dict, sort_keys=True))

    def filter_around(
        self,
        when: datetime,
        future: timedelta = timedelta(days=45),
        past: timedelta = timedelta(days=30),
    ) -> list[Event]:
        """Get a filtered list of events near the provided datetime.

        Joint events are collapsed to the first joint event found.
        """
        filtered_events = []
        future_timestamp = (when + future).timestamp() * 1000  # Need ms
        past_timestamp = (when - past).timestamp() * 1000  # Need ms

        ignored_joint_ids = set()
        for timestamp, events in sorted(self.events_by_time.items()):
            if timestamp > future_timestamp or timestamp < past_timestamp:
                continue

            for event in sorted(events, key=lambda e: e.id):
                if event.id in ignored_joint_ids:
                    continue

                filtered_events.append(event)

                if event.joint_with:
                    for joint_id in event.joint_with:
                        ignored_joint_ids.add(joint_id)

        filtered_events.sort(key=lambda e: e.time, reverse=True)

        return filtered_events

    def filter_group(
        self,
        group_slug: str,
        when: datetime,
        future: timedelta = timedelta(days=45),
        past: timedelta = timedelta(days=30),
    ) -> list[Event]:
        """Filter to a specific group.

        This isn't combined with `filter_around` because that method does extra
        handling for joint events that complicates group processing.
        """
        future_timestamp = (when + future).timestamp() * 1000  # Need ms
        past_timestamp = (when - past).timestamp() * 1000  # Need ms
        events = self.events_by_group[group_slug]
        return [
            event
            for event in sorted(events, key=lambda e: e.time, reverse=True)
            if past_timestamp <= event.time <= future_timestamp
        ]

    def all(self):
        for _, events in sorted(self.events_by_time.items()):
            for event in sorted(events, key=lambda e: e.id):
                yield event
