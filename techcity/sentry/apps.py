import sentry_sdk
from django.apps import AppConfig
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration


def traces_sampler(sampling_context):  # pragma: no cover
    """Select a sample rate off of the requested path.

    The root endpoint seemed to get hammered by some bot and ate a huge percent
    of transactions in a week. I don't care about that page right now,
    so ignore it.
    """
    path: str = sampling_context.get("wsgi_environ", {}).get("PATH_INFO", "")
    if (
        path == "/"
        or path.endswith(".php")
        or path.endswith(".php7")
        or path.startswith("/wp-")
    ):
        return 0

    return 1.0


class SentryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "techcity.sentry"

    def ready(self):  # pragma: no cover
        """Initialize Sentry.

        Sentry initialization is moved to an application ready timeframe
        because it triggers circular imports with settings
        under certain situations.
        """
        if not settings.SENTRY_ENABLED:
            return

        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
            ],
            traces_sampler=traces_sampler,
            send_default_pii=True,
        )
