from typing import Annotated

import typer

from techcity.events import FetchTriggered
from techcity.pubsub import publish


def fetch(
    cached: Annotated[
        bool,
        typer.Option(help="Use cached response data instead of fetching from sources"),
    ] = False,
) -> None:
    """Fetch data from API connections, normalize, and store in data directory."""
    publish(FetchTriggered(cached=cached))
