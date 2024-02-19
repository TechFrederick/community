from __future__ import annotations

from techcity.events import EventPublished
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
