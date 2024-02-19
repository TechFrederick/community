from techcity.events import BuildTriggered
from techcity.service import Service

from .build import build


class Builder(Service):
    consumes = [BuildTriggered]

    def dispatch(self, event) -> None:
        match event:
            case BuildTriggered():
                self.handle_build_triggered()

    def handle_build_triggered(self) -> None:
        build()
