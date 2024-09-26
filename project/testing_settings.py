from .settings import *  # noqa

# An in-memory database should be good enough for now.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

STORAGES = {
    "staticfiles": {
        # Whitenoise does not play well with tests
        # because tests don't run collectstatic.
        # Override back to the default storage for testing.
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# This eliminates the warning about a missing staticfiles directory.
WHITENOISE_AUTOREFRESH = True
