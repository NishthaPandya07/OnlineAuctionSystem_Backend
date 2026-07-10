from django.core.management.base import BaseCommand
from django.utils import timezone

from listings.models import Listing

from ...tasks import close_auction


class Command(BaseCommand):
    help = (
        'Close every active listing whose auction end time has passed. '
        'Intended to be run on a schedule (e.g. a cron entry every minute).'
    )

    def handle(self, *args, **options):
        expired = Listing.objects.filter(is_active=True, ends_at__lte=timezone.now())
        count = 0
        for listing in expired:
            close_auction(listing)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Closed {count} expired auction(s).'))
