from __future__ import annotations

from datetime import datetime, timedelta

from techcity.models import Event, EventListFilterOptions

from .service import EventsService


class EventsGateway:
    """A public synchronous interface for the events service"""

    def __init__(self, service: EventsService | None = None) -> None:
        self._service = service

    def connect(self, service: EventsService) -> None:
        """Connect to the events service."""
        self._service = service

    def all(self) -> list[Event]:
        if self._service is None:
            return []
        return self._service.list(EventListFilterOptions())

    def filter_around(self, when: datetime) -> list[Event]:
        if self._service is None:
            return []
        options = EventListFilterOptions(
            from_datetime=when - timedelta(days=30),
            to_datetime=when + timedelta(days=45),
        )
        return self._service.list(options)
