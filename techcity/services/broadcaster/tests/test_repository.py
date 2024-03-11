from techcity.models import BroadcastScheduleListFilterOptions, BroadcastScheduleStatus
from techcity.services.broadcaster.repository import BroadcastRepository
from techcity.testing.factories import BroadScheduleFactory


def test_ensure_broadcasts_dir(tmp_path):
    """The repository ensures that the broadcasts data storage area exists."""
    BroadcastRepository(tmp_path)
    broadcasts_dir = tmp_path / "broadcasts"

    assert broadcasts_dir.exists()


def test_create_stores_data(tmp_path):
    """A broadcast schedule is persisted to disk and updates the index."""
    repo = BroadcastRepository(tmp_path)
    schedule = BroadScheduleFactory.build()

    repo.create(schedule)

    schedule_path = tmp_path / "broadcasts" / f"{schedule.event_id}.yaml"
    assert schedule_path.exists()
    assert schedule.event_id in repo.schedules_by_id


def test_get(tmp_path):
    """The repo gets a schedule by its ID."""
    repo = BroadcastRepository(tmp_path)
    schedule = BroadScheduleFactory.build()
    repo.create(schedule)

    fetched_schedule = repo.get(schedule.event_id)

    assert fetched_schedule == schedule


def test_list_all(tmp_path):
    """All schedules are returned when there is no filtering."""
    repo = BroadcastRepository(tmp_path)
    repo.create(BroadScheduleFactory.build(status=BroadcastScheduleStatus.pending))
    repo.create(BroadScheduleFactory.build(status=BroadcastScheduleStatus.done))

    schedules = repo.list(BroadcastScheduleListFilterOptions())

    assert len(list(schedules)) == 2


def test_list_status(tmp_path):
    """Schedules matching the status are returned when there is status filtering."""
    repo = BroadcastRepository(tmp_path)
    pending_schedule = BroadScheduleFactory.build(
        status=BroadcastScheduleStatus.pending
    )
    repo.create(pending_schedule)
    repo.create(BroadScheduleFactory.build(status=BroadcastScheduleStatus.done))

    schedules = repo.list(
        BroadcastScheduleListFilterOptions(status=BroadcastScheduleStatus.pending)
    )

    assert list(schedules) == [pending_schedule]


def test_update_data(tmp_path):
    """A broadcast schedule is updated to disk and updates the index."""
    repo = BroadcastRepository(tmp_path)
    schedule = BroadScheduleFactory.build(status=BroadcastScheduleStatus.pending)
    repo.create(schedule)
    schedule.status = BroadcastScheduleStatus.done

    repo.update(schedule)

    updated_schedule = repo.get(schedule.event_id)
    assert updated_schedule is not None
    assert updated_schedule.status == BroadcastScheduleStatus.done
