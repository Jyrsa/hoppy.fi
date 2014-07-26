from django.core.management.base import BaseCommand, CommandError
from beerstatus.tasks  import refresh_beer_availability_statuses

class Command(BaseCommand):
    args = ''
    help = 'forces a beer availability update'

    def handle(self, *args, **options):
        refresh_beer_availability_statuses()
        self.stdout.write('Scheduled a beer availability update')
