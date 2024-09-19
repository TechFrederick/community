from __future__ import annotations

import datetime
from datetime import timedelta

from techcity.events import BroadcastTriggered, EventPublished
from techcity.models import (
    Broadcast,
    BroadcastSchedule,
    BroadcastScheduleListFilterOptions,
    BroadcastScheduleStatus,
    Event,
)
from techcity.service import Service
from techcity.services.broadcaster.channel import Channel
from techcity.services.events.gateway import EventsGateway

from .channels.console import ConsoleChannel
from .repository import BroadcastRepository


class Broadcaster(Service):
    """A service for broadcasting to social channels like Discord"""

    consumes = [BroadcastTriggered, EventPublished]

    def __init__(
        self,
        events_gateway: EventsGateway,
        repo: BroadcastRepository | None = None,
        channels: list[Channel] | None = None,
    ) -> None:
        self.events_gateway = events_gateway

        if repo is None:
            self.repo = BroadcastRepository()
        else:
            self.repo = repo

        if channels is None:
            # FIXME: The channels used should be driven by the configuration file.
            # I'm not solving that in this branch. Instead, we'll hardcode to use
            # the console channel to get something working.
            # self.channels = []
            self.channels = [ConsoleChannel()]
        else:
            self.channels = channels

    def dispatch(self, event) -> None:
        # FIXME Disable broadcast collection and triggering.
        # I don't think this is likely to continue in this form for long
        # and these are needlessly junking up the repo for now.
        match event:
            case BroadcastTriggered():
                # self._broadcast()
                pass
            case EventPublished():
                # self._schedule(event.event)
                pass

    def _broadcast(self):
        """Broadcast any pending and due broadcasts to the channels."""
        now = datetime.datetime.now(tz=datetime.UTC)
        options = BroadcastScheduleListFilterOptions(
            status=BroadcastScheduleStatus.pending
        )
        schedules = self.repo.list(options)
        for schedule in schedules:
            self._scan_schedule(schedule, now)

    def _scan_schedule(
        self, schedule: BroadcastSchedule, now: datetime.datetime
    ) -> None:
        """Scan the schedule for any pending broadcasts and take action."""
        changed = False

        for broadcast in schedule.broadcasts:
            if broadcast.scheduled_for > now or broadcast.sent_on is not None:
                continue

            # For now, broadcasting is going to punt on complex error handling.
            # This code optimistically assumes that all channel sending succeeds.
            # Eventually, we'll want to answer the question "Is a broadcast
            # successful if one of the channels fails?," but that can be solved
            # in the future.

            event = self.events_gateway.get(schedule.event_id)
            if event:
                self._send_broadcast(event)

            broadcast.sent_on = now
            changed = True

        # Finalize a schedule if all broadcasts are done.
        if all([broadcast.sent_on is not None for broadcast in schedule.broadcasts]):
            schedule.status = BroadcastScheduleStatus.done
            changed = True

        if changed:
            self.repo.update(schedule)

    def _send_broadcast(self, event: Event) -> None:
        """Send the event broadcast to all the channels."""
        for channel in self.channels:
            channel.send(event)

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
