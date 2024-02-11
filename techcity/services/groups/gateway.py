from __future__ import annotations
from .service import GroupsService


class GroupsGateway:
    """A public synchronous interface for the groups service"""

    def __init__(self, service: GroupsService | None = None) -> None:
        self._service = service

    def connect(self, service: GroupsService) -> None:
        """Connect to the groups service."""
        self._service = service
