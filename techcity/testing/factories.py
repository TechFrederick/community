from polyfactory.factories.pydantic_factory import ModelFactory

from techcity.models import BroadcastSchedule, Event, EventExtensions


class EventExtensionsFactory(ModelFactory[EventExtensions]): ...


class EventFactory(ModelFactory[Event]):
    extentions = EventExtensionsFactory


class BroadScheduleFactory(ModelFactory[BroadcastSchedule]): ...
