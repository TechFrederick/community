# Events

This document lists the public events that services in the system may react to.

## Command Events

### `BroadcastTriggered`

This event is emitted when an operator requests a broadcast for any event
that has scheduled broadcast messages that are pending.

### `BuildTriggered`

This event is emitted when an operator requests a build
of the web user interface content.

### `FetchTriggered`

This event is emitted when an operator requests a fetch of information
from outbound data sources.

## Integration Events

### `EventPublished`

A *physical* event (i.e., a meeting of people) is published.
This message may occur many times since details about the event may change
(for instance, a change in venue).
