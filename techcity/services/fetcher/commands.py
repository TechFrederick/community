import typer
from typing_extensions import Annotated

from techcity.events import FetchTriggered
from techcity.pubsub import publish


def fetch(
    cached: Annotated[
        bool,
        typer.Option(help="Use cached response data instead of fetching from sources"),
    ] = False
) -> None:
    """Trigger a fetch operation."""
    publish(FetchTriggered(cached=cached))
