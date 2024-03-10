import typer

from techcity.events import BroadcastTriggered


def broadcast(ctx: typer.Context) -> None:
    """Send out broadcast messages about any upcoming event."""
    pubsub = ctx.obj["pubsub"]
    pubsub.publish(BroadcastTriggered())
