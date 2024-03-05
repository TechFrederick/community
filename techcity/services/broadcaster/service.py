from __future__ import annotations

from techcity.events import EventPublished
from techcity.models import Event
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
        # TODO: create a broadcast schedule.
