from __future__ import annotations

from techcity.models import Group

from .service import GroupsService


class GroupsGateway:
    """A public synchronous interface for the groups service"""

    def __init__(self, service: GroupsService | None = None) -> None:
        self._service = service

    def connect(self, service: GroupsService) -> None:
        """Connect to the groups service."""
        self._service = service

    def all(self) -> list[Group]:
        if self._service is None:
            return []
        return self._service.all()

    def retrieve(self, slug: str) -> Group | None:
        if self._service is None:
            return None
        return self._service.retrieve(slug)
