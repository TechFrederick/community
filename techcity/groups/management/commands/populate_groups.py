from pathlib import Path

import requests
import stamina
from django.core.management.base import BaseCommand

from techcity.groups.models import Group


class Command(BaseCommand):
    help = "Fetch and upsert groups from the deployed API"

    def handle(self, *args, **kwargs):
        response = self.fetch_groups()
        groups = response.json()
        if groups:
            group_instances = [Group(**item) for item in groups]
            update_fields = [
                field.name
                for field in Group._meta.get_fields()
                if field.name != "id" and field.concrete
            ]
            Group.objects.bulk_create(
                group_instances,
                update_conflicts=True,
                unique_fields=["id"],
                update_fields=update_fields,
            )
            self.fetch_images(group_instances)
            self.stdout.write(self.style.SUCCESS("Successfully upserted groups table"))
        else:
            self.stdout.write(
                self.style.NOTICE("No groups returned, no records to add to db")
            )

    @stamina.retry(on=requests.RequestException)
    def fetch_groups(self):
        endpoint = "https://community.techfrederick.org/api/v1/groups"
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response

    def fetch_images(self, groups):
        """Fetch image data from the live site for each image field."""
        for group in groups:
            self.stdout.write(f"Fetching {group.name} card image...")
            self.fetch_image(group.card_image)

            self.stdout.write(f"Fetching {group.name} hero image...")
            self.fetch_image(group.hero_image)

    @stamina.retry(on=requests.RequestException)
    def fetch_image(self, image):
        image_path = Path(image.path)
        # Ensure that the right directory structure exists in the local destination.
        image_dir = image_path.parent
        image_dir.mkdir(exist_ok=True, parents=True)

        origin_domain = "https://community.techfrederick.org"
        response = requests.get(f"{origin_domain}{image.url}", stream=True, timeout=5)
        response.raise_for_status()
        with open(image_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
