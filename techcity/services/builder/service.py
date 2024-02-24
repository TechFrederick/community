from techcity.events import BuildTriggered
from techcity.service import Service
from techcity.services.events.gateway import EventsGateway
from techcity.services.groups.gateway import GroupsGateway

from .build import build


class Builder(Service):
    consumes = [BuildTriggered]

    def __init__(
        self,
        events_gateway: EventsGateway,
        groups_gateway: GroupsGateway,
    ):
        self.events_gateway = events_gateway
        self.groups_gateway = groups_gateway

    def dispatch(self, event) -> None:
        match event:
            case BuildTriggered():
                self.handle_build_triggered()

    def handle_build_triggered(self) -> None:
        build(self.events_gateway, self.groups_gateway)
