from pathlib import Path

from techcity import constants


class BroadcastRepository:
    def __init__(self, data_path: Path | None = None) -> None:
        if data_path is None:
            data_path = constants.data_path
        self.broadcasts_path = data_path / "broadcasts"
