from __future__ import annotations

from techcity.models import Event

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
        return self._service.list()
