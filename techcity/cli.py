import typer

from .build import build
from .pubsub import subscribe
from .services.events.service import EventsService
from .services.fetcher.commands import fetch
from .services.fetcher.service import Fetcher
from .services.groups.gateway import GroupsGateway
from .services.groups.service import GroupsService


def initialize():
    # Initialize the services and event bus.
    # Don't use a docstring here or else it will show in the CLI help text.

    groups_gateway = GroupsGateway()

    groups_service = GroupsService()
    services = [
        EventsService(),
        Fetcher(groups_gateway),
        groups_service,
    ]

    # In this synchronous model, connections are the only way that a
    # gateway can connect to the implementing service.
    # In a distributed future, a gatway may use some kind of transport client
    # (like an HTTP client or maybe a NATS client) to connect to a remote service.
    groups_gateway.connect(groups_service)

    subscribe(services)


app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    callback=initialize,
)
app.command()(build)
app.command()(fetch)
