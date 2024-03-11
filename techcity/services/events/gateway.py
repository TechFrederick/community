from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta

from techcity.models import Event, EventKind, EventListFilterOptions

from .service import EventsService


class EventsGateway:
    """A public synchronous interface for the events service"""

    def __init__(self, service: EventsService | None = None) -> None:
        self._service = service

    def connect(self, service: EventsService) -> None:
        """Connect to the events service."""
        self._service = service

    def get(self, event_id) -> Event | None:
        if self._service is None:
            return None
        return self._service.get(event_id)

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

    def filter_group(
        self, group_slug: str, from_datetime: datetime, to_datetime: datetime
    ):
        if self._service is None:
            return []
        options = EventListFilterOptions(
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            group_slug=group_slug,
        )
        return self._service.list(options)

    def filter_kind(self, kind: EventKind) -> Iterable[Event]:
        if self._service is None:
            return []
        options = EventListFilterOptions(kind=kind)
        return self._service.list(options)
