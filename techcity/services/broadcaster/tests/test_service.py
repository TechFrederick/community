import datetime
from unittest import mock

import time_machine

from techcity.events import EventPublished
from techcity.services.broadcaster.service import Broadcaster
from techcity.testing.factories import EventFactory


def test_default():
    """The default constructor uses a real repository."""
    service = Broadcaster()

    assert service.repo is not None


@time_machine.travel(datetime.datetime(2024, 3, 6, tzinfo=datetime.UTC))
def test_event_published_scheduled():
    """EventPublished sets a broadcast schedule."""
    repo = mock.Mock()
    service = Broadcaster(repo)
    start_at = datetime.datetime(2024, 3, 27, 21, tzinfo=datetime.UTC)
    event = EventFactory.build(start_at=start_at)
    event_published = EventPublished(event=event)

    service.dispatch(event_published)

    assert repo.create.called
    schedule = repo.create.call_args.args[0]
    assert len(schedule.broadcasts) == 3
