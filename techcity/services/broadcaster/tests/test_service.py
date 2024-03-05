from unittest import mock

from techcity.events import EventPublished
from techcity.services.broadcaster.service import Broadcaster
from techcity.testing.factories import EventFactory


def test_event_published_scheduled():
    """EventPublished sets a broadcast schedule."""
    repo = mock.Mock()
    service = Broadcaster(repo)
    event = EventFactory.build()
    event_published = EventPublished(event=event)

    service.dispatch(event_published)

    # TODO: assert that the broadcast schedule is created for the event.
