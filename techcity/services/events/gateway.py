from __future__ import annotations

from .service import EventsService


class EventsGateway:
    """A public synchronous interface for the events service"""

    def __init__(self, service: EventsService | None = None) -> None:
        self._service = service

    def connect(self, service: EventsService) -> None:
        """Connect to the events service."""
        self._service = service
