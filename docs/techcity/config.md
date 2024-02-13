# Configuration

Some configuration is required to make the techcity platform work
for individual cities.
This page covers the configuration settings.

## `timezone` (required)

Dates and times are stored internally using UTC.
To localize output to your city's timezone, use the `timezone` setting.
The platform handles daylight savings time automatically.

```toml
timezone = "US/Eastern"
```
