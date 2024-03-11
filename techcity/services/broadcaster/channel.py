from techcity.models import Event


class Channel:
    """A channel represents a method of sharing information to others.

    For instance, events could be broadcast to the channels of Discord, X,
    or Facebook. Channels are solely responsible for sending information
    to these external services.
    """

    def send(self, event: Event) -> bool:
        """Send information about an event via this channel to an external service.

        The channel should report back if the send was successful via the return.
        """
        raise NotImplementedError()
