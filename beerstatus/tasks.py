import logging

from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils import timezone
from huey.djhuey import db_periodic_task
from huey.djhuey import crontab
from huey.djhuey import db_task
import pytz
import requests
import json
import datetime
from . import models
from lxml import html
from django.utils.timezone import utc
import re

LOGGER = logging.getLogger(__name__)

@db_periodic_task(crontab(hour='/3'))
def refresh_beer_availability_statuses():
    LOGGER.info("starting beer status updates")
    for beer in models.Beer.objects.all().filter(active=True):
        for city_id, city in models.SUPPORTED_ALKO_CITIES:
            refresh_beer_availability(beer, city_id)
    LOGGER.info("finished scheduling beer status updates")

def parse_alko_availability_date(value):
    #alko servers are always in helsinki local time so references like 
    #yesterday etc. also follow that
    helsinki = pytz.timezone("Europe/Helsinki")
    date = datetime.datetime.utcnow().replace(tzinfo=utc).astimezone(helsinki)
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

def retrieve_etree(url):
    """ returns an lxml etree for the url given
    """
    #i would love to just request the floats in en-US
    #but alko doesn't honor the value consistently
    response = requests.get(url )
    tree = html.fromstring(response.text)
    return tree

def get_element_contents(tree, xpath, cure):
    """ takes in the tree, xpath and a curing function that should clean the
    value and/or coerce it into the right format (e.g. int(), float() or
    a lambda).
    
    raises an error if no element is found. Returns first element if several
    are found.
    """
    list_ = tree.xpath(xpath)
    if len(list_) == 0:
        raise ScrapeElementNotFoundException(
            "element not found %s" % xpath
            )
    return cure( list_[0])

class ScrapeInconsistencyException(BaseException):
    pass


class ScrapeElementNotFoundException(BaseException):
    pass

@db_periodic_task(crontab(hour='/12'))
def update_beer_infos():
    #loop through all after testing 
    for beer in models.Beer.objects.all():
        update_beer_info(beer)

@db_task()
def update_beer_info(beer):
    """ retrieves beer page from alko, updates model fields and saves model.

    Also retrieves name so that beer lists can be bootstrapped with just alko
    product IDs in the future. Doesn't update name if one exists.
    """
    beer_url ="http://www.alko.fi/en/products/%s/" % beer.alko_product_id
    tree = retrieve_etree(beer_url)
    #be careful when retrieving these xpaths using chrome's dev tools
    #chrome adds a tbody in the table that isn't present in the source and
    #that lxml doesn't add
    product_id = get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]/div[1]'
                    '/div[2]/div[6]/table/tr[1]/td[2]/text()'),
                    lambda x: x.strip()
                ).strip()
    if product_id != beer.alko_product_id:
        raise ScrapInconsistencyException(("attempted to get beer info for"
        "product %s but received info for product %s instead") %
        (beer.alko_product_id, product_id))
    product_category = get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]'
                    '/div[1]/div[2]/div[6]/h3/text()'),
                    lambda x: x.strip())
    if product_category != "beer":
        raise ScrapInconsistencyException(("attempted to get a beer but %s "
        "is of category %s ") % (product_id, product_category))
    abv = get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]/div[1]'
                    '/div[2]/div[6]/table/tr[2]/td[2]/text()'),
                    lambda x: float(x.replace('%', '').replace(",",".").strip())
                    )
    if abv < 0 or abv > 50:
        raise ScrapInconsistencyException(("abv is not logica for a beer"
        "produdct %d" % abv))
    ebu = get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]/div[1]'
                    '/div[2]/div[6]/table/tr[5]/td[2]/text()'),
                    lambda x: float(x.replace('EBU', '').replace(",", ".").strip())
                    )
    if ebu < 0 :
        raise ScrapInconsistencyException(("ebu is not logica for a beer"
        "produdct %d" % ebu))
    style =  get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]/div[1]'
                    '/div[2]/div[6]/table/tr[10]/td[2]/text()'),
                    lambda x: x.strip()
                    )
    #style info isn't in model yet so don't include it
    price =  get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]/'
                    'div[1]/div[2]/div[1]/span[1]/text()'),
                    lambda x: float(x.strip().replace(",","."))
                    )
    if price <= 0: 
        raise ScrapInconsistencyException(("beer price is <= 0."
        " There's no such thing as free beer!"))
    volume = get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/div[1]/'
                    'div[1]/div[2]/div[2]/text()'),
                    lambda x: float(x.strip().replace(",","."))
                    )
    if volume <= 0 or volume > 10:
        raise ScrapInconsistencyException(("Beer volume is not credible!"
        " There's no such thing as jottalitran tuopponen!"))
    name = get_element_contents(
                    tree,
                    ('/html/body/div[7]/div/div[1]/div/'
                    'div[1]/div[1]/div[2]/h1/text()'),
                    lambda x: x.strip()
                    )
    if volume <= 0 or volume > 200:
        raise ScrapInconsistencyException(("Beer name is incompatible: !"
        " %" ) % name)
    beer.abv = abv
    beer.ebu = ebu
    beer.price = price
    beer.volume = volume
    beer.style = style
    if not beer.name:
        beer.name = name
        beer.slug = slugify(name) 
    beer.save()

def find_alko_id_by_name(name):
    name = name.replace("Alko", "").strip()
    response = requests.get(
    "http://www.alko.fi/api/find/stores?Language=en&Page=0&PageSize=20&ProductIds=&Query=%s"
            % name)
    blob = response.json()
    results = blob.get("Results", [])
    if len(results) == 1:
        url = results[0]["Url"]
        match = re.search(r"\d{4}", url)
        if match:
            return match.group(0)
    return None

@db_periodic_task(crontab(hour="5"))
def update_all_alko_infos():
    for alko in models.AlkoLocation.objects.all():
        update_alko_info(alko)

@db_task()
def update_alko_info(alko):
    store_id = find_alko_id_by_name(alko.name) or alko.store_id
    if not store_id:
        logging.warning("no store_id found for store name "\
            + alko.name)
        return  #should this be a loud failure?
    alko.store_id = store_id
    alko.save() #save here so in case page is different
    #from standard we at least get id
    url ="http://www.alko.fi/en/shops/%s/" % store_id
    tree = retrieve_etree(url)
    streetaddr = ""
    try:
        streetaddr = get_element_contents(tree, 
            ('/html/body/div[7]/div/div[1]/div/div/'
            'div/div[2]/span[1]/div/span[1]/text()'), 
            lambda x: x)
    except ScrapeElementNotFoundException:
        pass
    areacode = ""
    try:
        areacode = get_element_contents(tree, 
            ('/html/body/div[7]/div/div[1]/div/div/'
            'div/div[2]/span[1]/div/span[2]/text()'), 
            lambda x: x)
    except ScrapeElementNotFoundException:
        pass
    city = ""
    try:
        city = get_element_contents(tree, 
            ('/html/body/div[7]/div/div[1]/div/div/'
            'div/div[2]/span[1]/div/span[3]/text()'), 
            lambda x: x)
    except ScrapeElementNotFoundException:
        pass
    address = "%s, %s %s" % (
                streetaddr,
                areacode,
                city
                )
    name = get_element_contents(tree, 
            ('/html/body/div[7]/div/div[1]/div/div/'
            'div/h1/text()'), 
            lambda x: x)
    # if name.length > 0:
    #     alko.name = name
    #     todo: should the name be used?
    if len(address) > 4:
        alko.address = address
    alko.save()
    
