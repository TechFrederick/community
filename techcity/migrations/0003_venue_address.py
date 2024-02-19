# This migration script converts all the events from their original
# Meetup ID to native ID that will be consistent on the platform.

import os

import yaml

for dirpath, _, filenames in os.walk("data/events"):
    for filename in filenames:
        event_filename = os.path.join(dirpath, filename)
        with open(event_filename) as f:
            event_data = yaml.safe_load(f)

        print(event_filename)
        if "venue" in event_data and event_data["venue"] is not None:
            event_data["venue"]["address"] = event_data["venue"]["address_1"]
            del event_data["venue"]["address_1"]

        with open(event_filename, "w") as f:
            f.write(yaml.dump(event_data, sort_keys=True))
