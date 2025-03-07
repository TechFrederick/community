from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from django.db import models
from django.templatetags.static import static


def favicon_image_path(instance, filename):
    path = Path(filename)
    return f"icons/favicon{path.suffix}"


def icon_192x192_image_path(instance, filename):
    path = Path(filename)
    return f"icons/192x192{path.suffix}"


def icon_512x512_image_path(instance, filename):
    path = Path(filename)
    return f"icons/512x512{path.suffix}"


def social_image_path(instance, filename):
    path = Path(filename)
    return f"images/social{path.suffix}"


class BrandQuerySet(models.QuerySet):
    def active(self) -> Brand:
        """Get the active brand instance"""
        brand = self.last()
        if brand:
            return brand
        return Brand(
            city="Techcity",
            url="https://github.com/TechFrederick/community",
            name="techcity Community",
            tagline="Join tech-minded people from your local area",
            description=(
                "techcity is a tool for connecting a technical community in a city."
            ),
        )


BrandManager = models.Manager.from_queryset(BrandQuerySet)


class Brand(models.Model):
    """Information that represents the city and how the site should display"""

    city = models.CharField(max_length=64)
    url = models.URLField(
        help_text="The full URL to the site (excluding the trailing slash)"
    )
    name = models.CharField(
        max_length=64, help_text="The name to use to describe the community"
    )
    tagline = models.CharField(
        max_length=128,
        help_text="The short phrase that acts as a compelling call to action",
    )
    description = models.TextField(
        help_text=(
            "A longer description to describe the community."
            " This should be a sentence or two."
        )
    )
    favicon = models.FileField(
        upload_to=favicon_image_path,
        help_text="A favicon file to use for the tab image",
    )
    icon_192x192 = models.FileField(
        upload_to=icon_192x192_image_path,
        help_text="An icon file to use for small contexts and progressive web apps",
    )
    icon_512x512 = models.FileField(
        upload_to=icon_512x512_image_path,
        help_text="An icon file to use for large contexts and progressive web apps",
    )
    social_image = models.FileField(
        upload_to=social_image_path,
        help_text="A social image file to use with social network embedding",
    )

    objects = BrandManager()

    @property
    def domain(self):
        return urlsplit(self.url).netloc

    @property
    def favicon_url(self):
        """Get the URL to the favicon with a safe static fallback."""
        if self.favicon:
            return self.favicon.url
        # TODO: replace with a default static file.
        return static("favicon.ico")

    @property
    def icon_192x192_url(self):
        """Get the URL to the 192x192 icon with a safe static fallback."""
        if self.icon_192x192:
            return self.icon_192x192.url
        # TODO: replace with a default static file.
        return static("300x300.webp")

    @property
    def icon_512x512_url(self):
        """Get the URL to the 512x512 icon with a safe static fallback."""
        if self.icon_512x512:
            return self.icon_512x512.url
        # TODO: replace with a default static file.
        return static("300x300.webp")

    @property
    def social_image_url(self):
        """Get the URL to the social iamge with a safe static fallback."""
        if self.social_image:
            return self.social_image.url
        # TODO: replace with a default static file.
        return static("images/og/techfrederick-community.png")
