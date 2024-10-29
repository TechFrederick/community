from django.urls import reverse


class TestGetGroups:
    def test_ok(self, client):
        response = client.get(reverse("api:get_groups"))

        assert response.status_code == 200
