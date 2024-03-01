from techcity.events import FetchTriggered
from techcity.pubsub import PubSub
from techcity.service import Service
from techcity.services.groups.gateway import GroupsGateway

from .fetch import fetch


class Fetcher(Service):
    consumes = [FetchTriggered]

    def __init__(
        self,
        pubsub: PubSub,
        groups_gateway: GroupsGateway,
    ):
        self.pubsub = pubsub
        self.groups_gateway = groups_gateway

    def dispatch(self, event) -> None:
        match event:
            case FetchTriggered():
                self.handle_fetch_triggered(event)

    def handle_fetch_triggered(self, event: FetchTriggered) -> None:
        fetch(event.cached, self.pubsub, self.groups_gateway)
