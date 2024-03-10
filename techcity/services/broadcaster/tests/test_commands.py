from unittest import mock

import typer
from click import Command

from techcity.events import BroadcastTriggered
from techcity.services.broadcaster.commands import broadcast


def test_publishes_broadcast_trigger():
    """The broadcast command publishes a BroadcastTriggered event."""
    pubsub = mock.Mock()
    ctx = typer.Context(Command("broadcast"), obj={})
    ctx.obj["pubsub"] = pubsub

    broadcast(ctx)

    event = pubsub.publish.call_args.args[0]
    assert isinstance(event, BroadcastTriggered)
