from pathlib import Path

import requests
import stamina
from django.core.management.base import BaseCommand

from techcity.core.models import Brand


class Command(BaseCommand):
    help = "Fetch and upsert the brand from the deployed API"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching brand...")
        response = self.fetch_brand()
        brand_data = response.json()
        city = brand_data.pop("city", "techcity")
        brand, _ = Brand.objects.update_or_create(city=city, defaults=brand_data)
        self.fetch_images(brand)

    @stamina.retry(on=requests.RequestException)
    def fetch_brand(self):
        endpoint = "https://community.techfrederick.org/api/v1/brand"
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response

    def fetch_images(self, brand):
        """Fetch image data from the live site for each image field."""
        self.stdout.write(f"Fetching {brand.name} favicon image...")
        self.fetch_image(brand.favicon)

        self.stdout.write(f"Fetching {brand.name} 192x192 icon image...")
        self.fetch_image(brand.icon_192x192)

        self.stdout.write(f"Fetching {brand.name} 512x512 icon image...")
        self.fetch_image(brand.icon_512x512)

        self.stdout.write(f"Fetching {brand.name} social image...")
        self.fetch_image(brand.social_image)

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
