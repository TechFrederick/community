import datetime
from unittest import mock

import pytest
import time_machine

from techcity.events import BroadcastTriggered, EventPublished
from techcity.services.broadcaster.channels.memory import MemoryChannel
from techcity.services.broadcaster.service import Broadcaster
from techcity.services.events.gateway import EventsGateway
from techcity.testing.factories import BroadScheduleFactory, EventFactory


def test_default():
    """The default constructor uses a real repository."""
    events_gateway = EventsGateway()
    service = Broadcaster(events_gateway)

    assert service.repo is not None


@time_machine.travel(datetime.datetime(2024, 3, 6, tzinfo=datetime.UTC))
def test_event_published_scheduled():
    """EventPublished sets a broadcast schedule."""
    events_gateway = EventsGateway()
    repo = mock.Mock()
    service = Broadcaster(events_gateway, repo)
    start_at = datetime.datetime(2024, 3, 27, 21, tzinfo=datetime.UTC)
    event = EventFactory.build(start_at=start_at)
    event_published = EventPublished(event=event)

    service.dispatch(event_published)

    assert repo.create.called
    schedule = repo.create.call_args.args[0]
    assert len(schedule.broadcasts) == 3


@time_machine.travel(datetime.datetime(2024, 3, 6, tzinfo=datetime.UTC))
def test_update_event_changed():
    """The schedule changes when the event is updated."""
    events_gateway = EventsGateway()
    repo = mock.Mock()
    service = Broadcaster(events_gateway, repo)
    start_at = datetime.datetime(2024, 3, 27, 21, tzinfo=datetime.UTC)
    original_event = EventFactory.build(start_at=start_at)
    original_schedule = BroadScheduleFactory.build(
        event_id=original_event.id, event_start_at=start_at
    )
    repo.get.return_value = original_schedule
    event = EventFactory.build(start_at=start_at + datetime.timedelta(days=7))
    event_published = EventPublished(event=event)

    service.dispatch(event_published)

    assert repo.create.called


@pytest.mark.xfail
def test_broadcasts_event():
    """A pending broadcast is sent on a channel."""
    events_gateway = EventsGateway()
    # TODO: set up an event and broadcast schedule with an event that needs
    # to broadcast.
    repo = mock.Mock()
    channel = MemoryChannel()
    service = Broadcaster(events_gateway, repo, channels=[channel])
    broadcast_triggered = BroadcastTriggered()

    service.dispatch(broadcast_triggered)

    assert len(channel.events_sent) == 1
    # TODO: assert that it's the event that we expect.
