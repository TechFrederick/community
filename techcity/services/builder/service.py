from techcity.events import BuildTriggered
from techcity.service import Service
from techcity.services.groups.gateway import GroupsGateway

from .build import build


class Builder(Service):
    consumes = [BuildTriggered]

    def __init__(
        self,
        groups_gateway: GroupsGateway,
    ):
        self.groups_gateway = groups_gateway

    def dispatch(self, event) -> None:
        match event:
            case BuildTriggered():
                self.handle_build_triggered()

    def handle_build_triggered(self) -> None:
        build(self.groups_gateway)
