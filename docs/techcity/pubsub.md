# Publish / Subscribe

The publish / subscribe pattern is a common way to do event-based communication.
With this pattern,
a system component like a service can publish messages about events
that occurred in the system
(e.g., a data fetching connector that scans for new in-person events
can publish an "Event Published" message when a new in-person event is available
in an API response).
The nice element of this pattern is that *publishers don't care who consumes
that event data*.

On the flip side,
consumers can register for an event type via a subscription.
Whenever a new event of that type occurs,
the pubsub will notify the subscriber of the new event
and the consumer can do whatever it needs with that data.
The subscriber *doesn't care who published the event data*.

Both the publishers and subscribers can be completely independent of each other,
requiring no knowledge that the other side exists.
The only things that matter are the events themselves,
which are [well-defined](events.md) and accessible to all services in the system.
