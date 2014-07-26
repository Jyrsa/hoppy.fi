from django.core.management.base import BaseCommand, CommandError
from beerstatus.models  import AlkoLocation
from beerstatus.tasks  import update_all_alko_infos

import csv

class Command(BaseCommand):
    args = 'csv_file'
    help = ('reads a csv file of alko locations and creates new'
            'stores as needed. implicitly queries alko website for more info')

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("this command takes in only one filename!")
        counter = 0
        with open(args[0], "r") as file_:
            reader = csv.DictReader(file_, [
                                            "latitude", 
                                            "longitude",
                                            "name",
                                            "city"
                                            ],
                                    )
            
            for entry in reader:
                created = self.make_or_update_location(entry)
                if created:
                    counter += 1
        update_all_alko_infos()
        self.stdout.write('updated values with %d new insertions' %counter)
    
    def make_or_update_location(self, vals):
        vals["name"] = vals["name"].strip()
        vals["city"] = vals["city"].strip()
        
        alko, created = AlkoLocation.objects.get_or_create(
                                        name=vals["name"].strip()
                                        )
        alko.latitude = float(vals["latitude"])
        alko.longitude = float(vals["longitude"])
        alko.city = vals["city"].lower()
        alko.save()
        return created


