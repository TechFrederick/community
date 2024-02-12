# Events

This document lists the public events that services in the system may react to.

## Command Events

### `FetchTriggered`

This event is emitted when an operator requests a fetch of information
from outbound data sources.

## Integration Events

### `EventPublished`

A *physical* event (i.e., a meeting of people) is published.
This message may occur many times since details about the event may change
(for instance, a change in venue).
