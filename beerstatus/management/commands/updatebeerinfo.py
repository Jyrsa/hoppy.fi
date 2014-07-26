from django.core.management.base import BaseCommand, CommandError
from beerstatus.tasks  import update_beer_infos

class Command(BaseCommand):
    args = ''
    help = 'forces a beer information update'

    def handle(self, *args, **options):
        update_beer_infos()
        self.stdout.write('Scheduled a beer availability update')
