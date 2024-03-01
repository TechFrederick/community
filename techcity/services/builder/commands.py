import typer

from techcity.events import BuildTriggered


def build(ctx: typer.Context) -> None:
    """Build the web UI by rendering all available content."""
    pubsub = ctx.obj["pubsub"]
    pubsub.publish(BuildTriggered())
