from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime

import yaml

from techcity.constants import data_path
from techcity.models import Event, EventListFilterOptions


class EventRepository:
    def __init__(self):
        self.events_path = data_path / "events"

        # Indices
        self.events_by_id: dict[str, Event] = {}
        self.events_by_group: defaultdict[str, set[Event]] = defaultdict(set)
        self.events_by_time = defaultdict(set)  # For joint event detection

        self._load_events()

    def _load_events(self):
        """Scan the events directory to load the events in memory."""
        for dir in sorted(self.events_path.glob("*")):
            group_slug = dir.name
            for event_filename in sorted(dir.glob("*")):
                with open(event_filename) as f:
                    event = Event(**yaml.load(f, Loader=yaml.Loader))  # noqa: S506

                self.events_by_id[event.id] = event
                self.events_by_group[group_slug].add(event)
                self.events_by_time[event.start_at].add(event)

    def create(self, event_data: dict) -> Event:
        """Create an event and persist it."""
        event = Event(**event_data)

        group_events = self.events_path / event.group_slug
        group_events.mkdir(exist_ok=True)

        self._update_indices(event)
        self._check_joint_events(event)
        self._save(group_events, event)
        return event

    def _update_indices(self, event: Event):
        """Update the indices of the repository.

        If this is not updated, then weird conditions can happen with other
        checking (e.g., adding multiple new events at once may have a mismatched
        `joint_with` set).
        """
        old_event = self.events_by_id.get(event.id)
        self.events_by_id[event.id] = event

        self.events_by_group[event.group_slug].add(event)
        if old_event:
            # There is a case where the event can change time and needs to move
            # to a different time set. Thus, we need to remove before adding,
            # which may look weird, but it's actually important.
            self.events_by_time[old_event.start_at].remove(old_event)
        self.events_by_time[event.start_at].add(event)

    def _check_joint_events(self, event):
        """Check if the event is a joint event with other groups.

        When a joint event is found, update linkages.
        """
        events = self.events_by_time[event.start_at]
        if len(events) <= 1:
            return

        # A joint event occurs when the two events are equal,
        # but have different identities.
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

    def list(self, options: EventListFilterOptions) -> Iterable[Event]:
        """Get a list of events."""
        if options.kind:
            return [
                event
                for event in self._filter_in(
                    from_datetime=options.from_datetime, to_datetime=options.to_datetime
                )
                if event.kind == options.kind
            ]
        if options.group_slug:
            return self._filter_group(
                options.group_slug,
                options.from_datetime,
                options.to_datetime,
            )
        elif options.from_datetime or options.to_datetime:
            return self._filter_in(options.from_datetime, options.to_datetime)
        else:
            return self._all()

    def _all(self):
        for _, events in sorted(self.events_by_time.items()):
            yield from sorted(events, key=lambda e: e.id)

    def _filter_in(
        self,
        from_datetime: datetime | None,
        to_datetime: datetime | None,
    ) -> list[Event]:
        """Get a filtered list of events near the provided datetime.

        Joint events are collapsed to the first joint event found.
        """
        filtered_events = []

        ignored_joint_ids = set()
        for start_at, events in sorted(self.events_by_time.items()):
            if (to_datetime and start_at > to_datetime) or (
                from_datetime and start_at < from_datetime
            ):
                continue

            for event in sorted(events, key=lambda e: e.id):
                if event.id in ignored_joint_ids:
                    continue

                filtered_events.append(event)

                if event.joint_with:
                    for joint_id in event.joint_with:
                        ignored_joint_ids.add(joint_id)

        filtered_events.sort(key=lambda e: e.start_at, reverse=True)

        return filtered_events

    def _filter_group(
        self,
        group_slug: str,
        from_datetime: datetime | None,
        to_datetime: datetime | None,
    ) -> Iterable[Event]:
        """Filter to a specific group.

        This isn't combined with `_filter_in` because that method does extra
        handling for joint events that complicates group processing.
        """
        events = self.events_by_group[group_slug]
        filtered_events: list[Event] = []
        for event in events:
            if (to_datetime and event.start_at > to_datetime) or (
                from_datetime and event.start_at < from_datetime
            ):
                continue

            filtered_events.append(event)

        return sorted(filtered_events, key=lambda e: e.start_at, reverse=True)
