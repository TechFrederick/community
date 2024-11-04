# Generated by Django 5.1.1 on 2024-11-01 02:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0003_alter_group_kind"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="event_source",
            field=models.CharField(
                choices=[
                    ("unspecified", "Unspecified"),
                    ("meetup", "Meetup"),
                    ("wordpress", "Wordpress"),
                ],
                default="unspecified",
                help_text="What is the source of event information for this group",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="event_source_id",
            field=models.CharField(
                blank=True,
                help_text="An optional ID to use when checking an event source",
                max_length=32,
            ),
        ),
    ]