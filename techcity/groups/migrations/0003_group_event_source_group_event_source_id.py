# Generated by Django 5.1.1 on 2024-09-21 19:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0002_group_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="event_source",
            field=models.CharField(
                default="",
                help_text="What is the source of event information for this group",
                max_length=16,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="group",
            name="event_source_id",
            field=models.CharField(
                default="",
                help_text="An optional ID to use when checking an event source",
                max_length=32,
            ),
            preserve_default=False,
        ),
    ]