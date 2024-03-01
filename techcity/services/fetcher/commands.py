from typing import Annotated

import typer

from techcity.events import FetchTriggered


def fetch(
    ctx: typer.Context,
    cached: Annotated[
        bool,
        typer.Option(help="Use cached response data instead of fetching from sources"),
    ] = False,
) -> None:
    """Fetch data from API connections, normalize, and store in data directory."""
    pubsub = ctx.obj["pubsub"]
    pubsub.publish(FetchTriggered(cached=cached))
