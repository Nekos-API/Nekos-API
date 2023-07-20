import subprocess, os, datetime

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

from django_bunny.storage import BunnyStorage


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Exporting database backup...")

        subprocess.call(f"PGPASSWORD=\"{os.getenv('PGPASSWORD')}\" pg_dump -U \"{os.getenv('PGUSER')}\" -h {os.getenv('PGHOST')} -d \"{os.getenv('PGDATABASE')}\" -f nekosapi_dump.sql", shell=True)
        
        self.stdout.write("Uploading backup to bunny...")
        
        storage = BunnyStorage(
            username=os.getenv("BUNNY_PRIVATE_USERNAME"),
            password=os.getenv("BUNNY_PRIVATE_PASSWORD"),
            region=os.getenv("BUNNY_PRIVATE_ZONE"),
        )

        with open("nekosapi_dump.sql", "rb") as f:
            storage.save(
                f"backups/backup-{str(datetime.datetime.utcnow().timestamp()).replace('.', '-')}.sql",
                f,
            )

        self.stdout.write("Done!")
