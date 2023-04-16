from django.core.management.base import BaseCommand, CommandError

from users.models import Domain


class Command(BaseCommand):
    help = "Checks for DNS records to verify domains."

    def handle(self, *args, **options):
        """
        Makes a DNS query for each domain to check if it has been verified.
        """

        for domain in Domain.objects.all():
            verified = domain.verify()
            self.stdout.write(
                domain.name
                + " - "
                + (
                    self.style.SUCCESS("VERIFIED")
                    if verified
                    else self.style.ERROR("NOT VERIFIED")
                )
            )
