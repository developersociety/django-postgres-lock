import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres_lock_{}".format(os.environ.get("TOX_ENV_NAME", "default")),
    }
}

SECRET_KEY = "postgres_lock"

INSTALLED_APPS = ["postgres_lock", "tests"]
