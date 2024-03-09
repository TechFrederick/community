from __future__ import annotations

import datetime
from datetime import timedelta

from techcity.events import EventPublished
from techcity.models import Broadcast, BroadcastSchedule, Event
from techcity.service import Service

from .repository import BroadcastRepository


class Broadcaster(Service):
    """A service for broadcasting to social channels like Discord"""

    consumes = [EventPublished]

    def __init__(self, repo: BroadcastRepository | None = None) -> None:
        if repo is None:
            self.repo = BroadcastRepository()
        else:
            self.repo = repo

    def dispatch(self, event) -> None:
        match event:
            case EventPublished():
                self._schedule(event.event)

    def _schedule(self, event: Event) -> None:
        """Set an event's broadcast schedule."""
        # Only update when the time changes or the event is not tracked.
        # If the schedule were updated every time, then broadcasts would be
        # chopped off as `now` passes older broadcast `scheduled_for` dates.
        current_schedule = self.repo.get(event.id)
        if (
            current_schedule is None
            or current_schedule.event_start_at != event.start_at
        ):
            # The broadcast frequency should probably be configurable in the future,
            # but these time frequencies are reasonable for now.
            broadcast_offsets = [
                timedelta(days=14),
                timedelta(days=7),
                timedelta(days=1),
            ]
            broadcasts = [
                Broadcast(scheduled_for=event.start_at - offset)
                for offset in broadcast_offsets
                # Sometimes events are created late. Don't create a broadcast if the
                # broadcast would be in the past.
                if event.start_at - offset > datetime.datetime.now(tz=datetime.UTC)
            ]

            # FIXME: I think it's possible that the broadcasts are not going to fire
            # on the expected date because the schedule_for is set on a day boundary.
            # For example, timedelta(days=1) should make an announcement the day
            # before an event. Since broadcasting in CI is in the very early morning,
            # going 24 hours before the event may not be early enough to hit the
            # broadcast window. We may be able get around that by pulling the
            # schedule_for to midnight of that day, but I want to think through
            # the implications of that before codifying it.

            schedule = BroadcastSchedule(
                event_id=event.id,
                event_start_at=event.start_at,
                broadcasts=broadcasts,
            )
            self.repo.create(schedule)
