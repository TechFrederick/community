from django.urls import reverse

from techcity.groups.tests.factories import GroupFactory


class TestGetGroups:
    def test_ok(self, client):
        GroupFactory()

        response = client.get(reverse("api:groups"))

        assert response.status_code == 200

        response_payload = response.json()
        assert isinstance(response_payload, list)
        assert len(response_payload) > 0
