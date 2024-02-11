import typer

from .build import build
from .pubsub import subscribe
from .services.fetcher.commands import fetch
from .services.fetcher.service import Fetcher


def initialize():
    # Initialize the services and event bus.
    # Don't use a docstring here or else it will show in the CLI help text.
    services = [
        Fetcher(),
    ]
    subscribe(services)


app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    callback=initialize,
)
app.command()(build)
app.command()(fetch)
