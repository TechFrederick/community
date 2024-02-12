# Gateways

The gateway pattern is a method to give an interface to an external system.
In the context of techcity, a gateway is used when a service needs to do
synchronous communication with another service.
Instead of invoking the other service's methods directly,
the gateway mediates this communication.
By doing this, we can achieve:

* A clear perspective on what a service's synchronous public API is
* A way to handle dependency injection to permit mock gateways for testing
* A flexible interface that can be changed in the future if the deployment
  architecture changes (e.g., services move to being over a network boundary)
