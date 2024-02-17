# This migration script converts all the events from their original
# Meetup ID to native ID that will be consistent on the platform.

import os

import yaml

from techcity.ids import generate_id

for dirpath, _, filenames in os.walk("data/events"):
    for filename in filenames:
        event_filename = os.path.join(dirpath, filename)
        with open(event_filename, "r") as f:
            event_data = yaml.safe_load(f)

        print(event_filename)
        # Set the new ID.
        old_id = event_data["id"]
        new_id = generate_id(old_id, "meetup")
        event_data["id"] = new_id

        # Create the new extension section.
        event_data["extensions"] = {"meetup": {"id": old_id}}

        # Set the joint_with IDs.
        new_joint_with = []
        for joint_with_id in event_data["joint_with"]:
            new_joint_with.append(generate_id(joint_with_id, "meetup"))
        new_joint_with.sort()
        event_data["joint_with"] = new_joint_with

        with open(os.path.join(dirpath, f"{new_id}.yaml"), "w") as f:
            f.write(yaml.dump(event_data, sort_keys=True))

        os.remove(event_filename)
