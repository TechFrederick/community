from __future__ import annotations

from techcity.events import EventPublished
from techcity.models import Event, EventListFilterOptions
from techcity.service import Service

from .repository import EventRepository


class EventsService(Service):
    """A service for handling physical events information"""

    consumes = [EventPublished]

    def __init__(self, repo: EventRepository | None = None) -> None:
        if repo is None:
            self.repo = EventRepository()
        else:
            self.repo = repo

    def dispatch(self, event) -> None:
        match event:
            case EventPublished():
                self.repo.create(event.event.model_dump())

    def get(self, event_id: str) -> Event | None:
        return self.repo.get(event_id)

    def list(self, options: EventListFilterOptions) -> list[Event]:
        """Get a list of events."""
        return list(self.repo.list(options))
