from collections import defaultdict

# Module level state is not awesome, but it should work for now.
event_registry = defaultdict(list)


def subscribe(services: list) -> None:
    """Subscribe each service to its list of events that it consumes."""
    for service in services:
        for event_cls in service.consumes:
            event_registry[event_cls].append(service)


def publish(event) -> None:
    """Publish an event to registered services.

    This implementation is a synchronous interface. It's a very crude method
    of decoupling and will crash multiple services if there is an error,
    but it has the benefit that the publisher doesn't need to know who the
    consuming services are.
    """
    services = event_registry.get(event.__class__)
    if services:
        for service in services:
            service.dispatch(event)
