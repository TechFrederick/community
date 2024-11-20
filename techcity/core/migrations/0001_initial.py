# Generated by Django 5.1.1 on 2024-11-20 05:20

from django.db import migrations, models

import techcity.core.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=64)),
                (
                    "url",
                    models.URLField(
                        help_text="The full URL to the site (including the trailing slash)"  # noqa
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name to use to describe the community",
                        max_length=64,
                    ),
                ),
                (
                    "tagline",
                    models.CharField(
                        help_text="The short phrase that acts as a compelling call to action",  # noqa
                        max_length=128,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="A longer description to describe the community. This should be a sentence or two."  # noqa
                    ),
                ),
                (
                    "favicon",
                    models.FileField(
                        help_text="A favicon file to use for the tab image",
                        upload_to=techcity.core.models.favicon_image_path,
                    ),
                ),
                (
                    "icon_192x192",
                    models.FileField(
                        help_text="An icon file to use for small contexts and progressive web apps",  # noqa
                        upload_to=techcity.core.models.icon_192x192_image_path,
                    ),
                ),
                (
                    "icon_512x512",
                    models.FileField(
                        help_text="An icon file to use for large contexts and progressive web apps",  # noqa
                        upload_to=techcity.core.models.icon_512x512_image_path,
                    ),
                ),
                (
                    "social_image",
                    models.FileField(
                        help_text="A social image file to use with social network embedding",  # noqa
                        upload_to=techcity.core.models.social_image_path,
                    ),
                ),
            ],
        ),
    ]
