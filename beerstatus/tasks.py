import logging

from django.conf import settings
from django.utils import timezone
from huey.djhuey import db_periodic_task
from huey.djhuey import crontab
from huey.djhuey import db_task
import pytz
import requests
import json
import datetime
from . import models

LOGGER = logging.getLOGGER(__name__)

@db_periodic_task(crontab(minute='*'))
def refresh_beers():
    LOGGER.info("starting beer status updates")
    for beer in models.Beer.objects.all().filter(active=True):
        for city_id, city in models.SUPPORTED_ALKO_CITIES:
            refresh_beer_availability(beer, city_id)
    LOGGER.info("finished scheduling beer status updates")

def parse_alko_availability_date(value):
    #alko servers are always in helsinki local time so references like 
    #yesterday etc. also follow that
    helsinki = pytz.timezone("Europe/Helsinki")
    date = datetime.datetime.now().astimezone(helsinki)
    if value == "today":
        return date
    if value == "yesterday":
        return date - datetime.timedelta(days=1)
    else:
        try:
            parts = value.split(".")[:2]
            if len(parts) == 2:
                day, month = parts
                day, month = int(day), int(month)
                date = datetime.datetime.now().date()
                for i in range(7): #accept up to 1 week old info
                    potential = date - datetime.timedelta(days=i)
                    if potential.day == day and potential.month == month:
                        date = potential
                        break
        except ValueError:
            pass


@db_task()
def refresh_beer_availability(beer, cityID):
    LOGGER.debug("refreshing beer %s status for %s" % (
                                                beer.name,
                                                cityID))
    url = \
    "http://www.alko.fi/api/product/Availability?productId=%s&cityId=%s&language=en"
    url = url % (beer.alko_product_id, cityID)
    response = requests.get(url)
    all_available = 0
    blob_list = response.json()
    for entry in blob_list:
        store_id = entry["StoreLink"].split("/")[-2]
        try:
            store = models.AlkoLocation.objects.get(store_id=store_id)
        except models.AlkoLocation.DoesNotExist:
            continue
        date = parse_alko_availability_date(entry["LastUpdated"])
        if not date:
            #
            return
        try:
            amount = int(entry["Amount"])
        except ValueError:
            continue
        all_available += amount
        avail, created = models.BeerAvailability.objects.get_or_create(
                        beer=beer,
                        location=store,
                        count=amount,
                        date=date
                        )
        avail.save()
    LOGGER.debug(("finished refreshing beer %s status for %s, "
                " found alltogether %d units") % (
                                                beer.name,
                                                cityID,
                                                all_available))
