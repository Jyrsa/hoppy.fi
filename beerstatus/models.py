from django.db import models
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from util import validate_integer
from util import validate_takes_one_string

class Beer(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name")
    ibu = models.FloatField(
                help_text=("International Bittering Units"),
                #this may not be available,
                default=0)
    #but alko offers both of these
    ebu = models.FloatField(
                help_text=("European Bitterness Units")
                )
    abv = models.FloatField(
                help_text=("Alcohol by Volume")
                )
    active = models.BooleanField(
                default=True,
                help_text = ("used to e.g. disclude "
                    "discontinued products from queries. set manually."
                    )
                )
    price = models.FloatField(default=0)
    volume = models.FloatField(default=.33, help_text=("volume in "
                    " litres"))
    alko_product_id = models.CharField(
                            max_length=6,
                            validators=[validate_integer]) 
    # should be an integer
    # todo: enforce check
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #Todo: add price info at some point
    #Todo: add style info at some point
    #However beer style is far from agreed on :(

    def __unicode__(self):
        return u"'%s' (%s ABV, %s EBU)" % (self.name,
                                            str(self.abv),
                                            str(self.ebu)
                            )


class BeerRater(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    url_base = models.CharField(max_length=400,
                validators=[validate_takes_one_string],
                default="http://localhost/?q=%s")  
    def __unicode__(self):
        return  self.name

    def get_url(self, foreign_id):
        """attempts to make a url for beer
        """
        return self.url_base % str(foreign_id)

class BeerRating(models.Model):
    beer = models.ForeignKey(Beer)
    rater = models.ForeignKey(BeerRater)
    foreign_id = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(
                help_text=("this content will come from"
                "RateBeer assuming it's ok with them. Start"
                " with manual entry and work to automated scraping"
                "/API")
                )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (('beer', 'rater'))
    
    def __unicode__(self):
        return u"%s given  %d points by %s" % (self.beer.name, 
                                            self.rating,
                                            self.rater.name,)

SUPPORTED_ALKO_CITIES = (
        ("espoo", "Espoo"),
        ("helsinki", "Helsinki")
        #ToDo, complete
        #Note that not all availability info is available
    )

class AlkoLocation(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name")
    city = models.CharField(max_length=200, choices=SUPPORTED_ALKO_CITIES)
    #alko stores have a www.alko.fi/myymalat/store_id/ address
    store_id = models.CharField(max_length=5, validators=[validate_integer],
    unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return u"%s, %s" % (
                                            self.name,
                                            self.address
                                            )
    def get_latest_beers_and_availability():
        values = [] 
        for beer in Beer.objects.filter(active=True):
            try:
                avail = BeerAvailability.objects.filter(beer=beer, 
                        location=self).order_by('-date')[0]
            except IndexError:
                continue
            values.append(beer, avail) 
        return values

    
class BeerAvailability(models.Model):
    beer = models.ForeignKey(Beer)
    location = models.ForeignKey(AlkoLocation)
    count = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

 
    def __unicode__(self):
        return u"Beer Availability %d bottles of %s at %s " % (
                                            self.count,
                                            self.beer.name,
                                            self.location.name, 
                                            )
   
     
