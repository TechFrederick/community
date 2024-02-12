from techcity.models import Group
from techcity.service import Service

from .repository import GroupRepository


class GroupsService(Service):
    """A service for handling groups information"""

    def __init__(self, repo: GroupRepository | None = None) -> None:
        if repo is None:
            self.repo = GroupRepository()
        else:
            self.repo = repo

    def all(self) -> list[Group]:
        return self.repo.all()
