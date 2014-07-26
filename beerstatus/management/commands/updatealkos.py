from django.core.management.base import BaseCommand, CommandError
from beerstatus.tasks  import update_all_alko_infos

class Command(BaseCommand):
    args = ''
    help = 'forces an alko info update'

    def handle(self, *args, **options):
        update_all_alko_infos()
        self.stdout.write('Scheduled alko info update')
