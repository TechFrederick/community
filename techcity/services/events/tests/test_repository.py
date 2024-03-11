from techcity.services.events.repository import EventRepository
from techcity.testing.factories import EventFactory


def test_ensure_events_dir(tmp_path):
    """The repository ensures that the events data storage area exists."""
    EventRepository(tmp_path)
    events_dir = tmp_path / "events"

    assert events_dir.exists()


def test_create_stores_data(tmp_path):
    """An event is persisted to disk and update the index."""
    repo = EventRepository(tmp_path)
    event = EventFactory.build()

    repo.create(event.model_dump())

    event_path = tmp_path / "events" / event.group_slug / f"{event.id}.yaml"
    assert event_path.exists()
    assert event.id in repo.events_by_id


def test_get(tmp_path):
    """The repo gets an event by its ID."""
    repo = EventRepository(tmp_path)
    event = EventFactory.build()
    repo.create(event.model_dump())

    fetched_event = repo.get(event.id)

    assert fetched_event == event
