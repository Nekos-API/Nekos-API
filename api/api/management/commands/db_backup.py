import subprocess, os, datetime

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

from django_bunny.storage import BunnyStorage

from nekos_api.utils import getsecret


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Exporting database backup...")

        subprocess.call(
            f"PGPASSWORD=\"{getsecret('DATABASE_PASSWORD')}\" pg_dump -U \"{os.getenv('DATABASE_USER')}\" -h {os.getenv('DATABASE_HOST')} -d \"{os.getenv('DATABASE_NAME')}\" -f nekosapi_dump.sql",
            shell=True,
        )

        self.stdout.write("Uploading backup to bunny...")

        storage = BunnyStorage(
            username=os.getenv("BACKEND_BUNNY_PRIVATE_USERNAME"),
            password=os.getenv("BACKEND_BUNNY_PRIVATE_PASSWORD"),
            region=os.getenv("BACKEND_BUNNY_PRIVATE_ZONE"),
        )

        with open("nekosapi_dump.sql", "rb") as f:
            storage.save(
                f"backups/backup-{str(datetime.datetime.utcnow().timestamp()).replace('.', '-')}.sql",
                f,
            )

        self.stdout.write("Done!")
