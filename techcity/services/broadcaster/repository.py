from pathlib import Path

import yaml

from techcity import constants
from techcity.models import BroadcastSchedule


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
                schedule = BroadcastSchedule(**yaml.load(f, Loader=yaml.Loader))  # noqa: S506
            self.schedules_by_id[schedule.event_id] = schedule

    def create(self, schedule: BroadcastSchedule) -> BroadcastSchedule:
        """Persist a broadcast schedule."""
        schedule_dict = schedule.model_dump()
        outpath = self.broadcasts_path / f"{schedule.event_id}.yaml"
        with open(outpath, "w") as f:
            f.write(yaml.dump(schedule_dict, sort_keys=True))
        return schedule
