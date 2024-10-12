from django.core.management import call_command
from huey import crontab
from huey.contrib.djhuey import db_periodic_task


@db_periodic_task(crontab(minute="0", hour="*/4"))
def fetch():
    """Delegate to a management command so that event fetching can be done manually."""
    call_command("fetch_events")
