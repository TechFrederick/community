import zoneinfo
import tomllib
from pathlib import Path


class ConfigError(Exception):
    pass


class Config:
    def __init__(self):
        self._timezone = ""
        self._tz = zoneinfo.ZoneInfo("UTC")

    @property
    def timezone(self) -> str:
        return self._timezone

    @timezone.setter
    def timezone(self, value: str) -> None:
        self._timezone = value
        self._tz = zoneinfo.ZoneInfo(value)

    @property
    def tz(self) -> zoneinfo.ZoneInfo:
        return self._tz


config = Config()


def load_config():
    """Load the configuration from the config file."""
    config_path = Path.cwd() / "techcity.toml"
    if not config_path.exists():
        raise ConfigError(f"Expected configuration file at {config_path}")

    with open(config_path, "rb") as f:
        try:
            config_data = tomllib.load(f)
        except tomllib.TOMLDecodeError as ex:
            raise ConfigError(f"Failed to load config file: {ex}")

    if "timezone" not in config_data:
        raise ConfigError("Missing required config setting: timezone")

    config.timezone = config_data["timezone"]
