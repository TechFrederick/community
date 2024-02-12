# Services

By splitting functionality of the techcity platform into services,
we can think through the system as distinct components
that interact with each other through very specific interfaces.
Stated explicitly,
services should only interact with each other through one of:

* Event messages via [publish/subscribe](pubsub.md)
* Well-defined public APIs via [gateways](gatways.md)

The goal of dividing the system this way is to create a clear software architecture,
while gaining the benefits of speed that come
from all source code living in the same code repository.
We can achieve a [Modular Monolith](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)
that can allow different parts of the system to evolve independently.

Also,
if there is ever a desire to split out into a different architectural style
(like a set of microservices),
that would be a lot more achievable with a modular monolith.

## Catalog

The set of services is small enough for now that all foreseeable services are listed
on this page.
As the system grows,
we may wish to split the catalog up.

### Events Service

The events service is a data service that handles functionality
related to the management of events.
These events are referring to in-person, physical events for humans,
not the kind of events that are happening in an event-based software system.

### Fetcher

The fetcher service is responsible for handling the fetch command trigger.
When triggered,
the service executes each configured connector
to make the desired outbound API calls.
The connectors process API data and emit any relevant system events.

### Groups Service

The groups service is a data service that handles functionality
related to the management of groups.
