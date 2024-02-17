# This file isn't truly needed, but this was the script used to do a data
# conversion on the model change. Data migration may need clear handling
# in the future and this could serve as a reference to what was done
# when the Event.time fields were changed to UTC datetimes.

import os
import zoneinfo
import datetime

import yaml

tz = zoneinfo.ZoneInfo("US/Eastern")

for dirpath, _, filenames in os.walk("data/events"):
    for filename in filenames:
        event_filename = os.path.join(dirpath, filename)
        with open(event_filename, "r") as f:
            event_data = yaml.safe_load(f)

        print(event_filename)

        start_at = datetime.datetime.fromtimestamp(
            event_data["time"] / 1000, tz=datetime.UTC
        )
        end_at = start_at + datetime.timedelta(milliseconds=event_data["duration"])
        event_data["start_at"] = start_at
        event_data["end_at"] = end_at

        del event_data["time"]
        del event_data["utc_offset"]
        del event_data["duration"]

        with open(event_filename, "w") as f:
            f.write(yaml.dump(event_data, sort_keys=True))

        # print(start_at)
        # print(start_at.astimezone(tz))
        # print(end_at.astimezone(tz))
