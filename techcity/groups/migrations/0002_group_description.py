# Generated by Django 5.1.1 on 2024-09-19 03:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="description",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
