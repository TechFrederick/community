from datetime import timedelta

import factory
from django.utils import timezone


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "events.Event"

    group = factory.SubFactory("techcity.groups.tests.factories.GroupFactory")
    start_at = factory.LazyFunction(timezone.localtime)
    end_at = factory.LazyAttribute(lambda e: e.start_at + timedelta(hours=2))
