import requests
from django.core.management.base import BaseCommand
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from techcity.groups.models import Group


class Command(BaseCommand):
    help = "Fetch and upsert groups from the deployed API"

    def handle(self, *args, **kwargs):
        groups_endpoint = "https://community.techfrederick.org/api/v1/groups"
        retries = Retry(
            total=3,
            allowed_methods={"GET"},
            status_forcelist=[502, 503, 504],
            backoff_factor=0.1,
        )
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            groups_response = session.get(groups_endpoint)
            groups_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.NOTICE(f"An error occurred: {e}, check {groups_endpoint}")
            )
            return

        groups = groups_response.json()
        if not groups:
            self.stdout.write(
                self.style.NOTICE(
                    f"No records returned from {groups_endpoint}, "
                    "no records to add to db"
                )
            )
            return
        else:
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
            self.stdout.write(self.style.SUCCESS("Successfully upserted groups table"))
