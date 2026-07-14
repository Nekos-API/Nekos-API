import os

from dotenv import load_dotenv


load_dotenv()


DEBUG = os.getenv("NEKOS_DEBUG", "False").lower() in ("true", "1", "t")


DATABASE = {
    "connections": {
        "default": os.getenv("NEKOS_DATABASE_URL", "sqlite://db.sqlite3"),
    },
    "apps": {
        "models": {
            "models": [
                "nekos_api.db.models.images",
            ],
            "default_connection": "default",
            "migrations": "nekos_api.db.migrations",
        }
    },
    "timezone": "UTC",
}


ADMIN_TOKEN = os.getenv("NEKOS_ADMIN_TOKEN")
"""The token that will be required for admin-only endpoints.

If not set (i.e. `None` or an empty string), admin-only endpoints will be disabled.
"""
