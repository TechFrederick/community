from techcity.events import FetchTriggered
from techcity.service import Service

from .fetch import fetch


class Fetcher(Service):
    consumes = [FetchTriggered]

    def dispatch(self, event) -> None:
        match event:
            case FetchTriggered:
                self.handle_fetch_triggered(event)

    def handle_fetch_triggered(self, event: FetchTriggered) -> None:
        fetch(event.cached)
