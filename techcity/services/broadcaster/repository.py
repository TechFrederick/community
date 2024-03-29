from collections.abc import Iterable
from pathlib import Path

import yaml

from techcity import constants
from techcity.models import BroadcastSchedule, BroadcastScheduleListFilterOptions


class BroadcastRepository:
    def __init__(self, data_path: Path | None = None) -> None:
        if data_path is None:
            data_path = constants.data_path
        self.broadcasts_path = data_path / "broadcasts"
        self.broadcasts_path.mkdir(exist_ok=True)

        self.schedules_by_id: dict[str, BroadcastSchedule] = {}
        self._load_schedules()

    def _load_schedules(self):
        """Scan the data directory to load the schedules in memory."""
        for schedule_filename in sorted(self.broadcasts_path.glob("*")):
            with open(schedule_filename) as f:
                schedule = BroadcastSchedule(
                    **yaml.load(f, Loader=yaml.Loader)  # noqa: S506
                )
            self.schedules_by_id[schedule.event_id] = schedule

    def create(self, schedule: BroadcastSchedule) -> BroadcastSchedule:
        """Persist a broadcast schedule."""
        return self._save(schedule)

    def _save(self, schedule: BroadcastSchedule) -> BroadcastSchedule:
        schedule_dict = schedule.model_dump()
        outpath = self.broadcasts_path / f"{schedule.event_id}.yaml"
        with open(outpath, "w") as f:
            f.write(yaml.dump(schedule_dict, sort_keys=True))

        self.schedules_by_id[schedule.event_id] = schedule
        return schedule

    def get(self, event_id: str) -> BroadcastSchedule | None:
        """Get a broadcast schedule.

        The event ID serves as the primary key.
        """
        return self.schedules_by_id.get(event_id)

    def list(
        self, options: BroadcastScheduleListFilterOptions
    ) -> Iterable[BroadcastSchedule]:
        """Get a list of broadcast schedules."""
        if options.status is not None:
            return [
                schedule
                for schedule in self.schedules_by_id.values()
                if schedule.status == options.status
            ]
        return self.schedules_by_id.values()

    def update(self, schedule: BroadcastSchedule) -> BroadcastSchedule:
        """Update a broadcast schedule.

        This has the same implementation as `create`, but is kept as a separate
        method in case needs diverge.
        """
        return self._save(schedule)
