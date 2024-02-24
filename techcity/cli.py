import typer
from rich import print

from .configuration import ConfigError, load_config
from .pubsub import subscribe
from .services.builder.commands import build
from .services.builder.service import Builder
from .services.events.gateway import EventsGateway
from .services.events.service import EventsService
from .services.fetcher.commands import fetch
from .services.fetcher.service import Fetcher
from .services.groups.gateway import GroupsGateway
from .services.groups.service import GroupsService


def initialize():
    # Initialize the services and event bus.
    # Don't use a docstring here or else it will show in the CLI help text.
    try:
        load_config()
    except ConfigError as ex:
        print(f"[red]{ex}[/red]")
        raise typer.Exit(code=1) from ex

    events_gateway = EventsGateway()
    groups_gateway = GroupsGateway()

    events_service = EventsService()
    groups_service = GroupsService()
    services = [
        Builder(events_gateway, groups_gateway),
        events_service,
        Fetcher(groups_gateway),
        groups_service,
    ]

    # In this synchronous model, connections are the only way that a
    # gateway can connect to the implementing service.
    # In a distributed future, a gatway may use some kind of transport client
    # (like an HTTP client or maybe a NATS client) to connect to a remote service.
    events_gateway.connect(events_service)
    groups_gateway.connect(groups_service)

    subscribe(services)


app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    callback=initialize,
)
app.command()(build)
app.command()(fetch)
