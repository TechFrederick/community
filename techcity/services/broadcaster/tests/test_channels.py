import pytest

from techcity.services.broadcaster.channel import Channel
from techcity.services.broadcaster.channels.memory import MemoryChannel
from techcity.testing.factories import EventFactory


def test_channel_interface():
    """A channel expects an implementation of the send interface."""
    channel = Channel()
    event = EventFactory.build()

    with pytest.raises(NotImplementedError):
        channel.send(event)


def test_memory_channel():
    """The in-memory channel captures an sent events."""
    memory_channel = MemoryChannel()
    event = EventFactory.build()

    sent = memory_channel.send(event)

    assert sent
    assert memory_channel.events_sent[0] == event
