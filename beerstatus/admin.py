""" The admin definitions.
"""

from django.contrib import admin

# Register your models here.

from models import Beer
from models import BeerRating
from models import BeerRater
from models import AlkoLocation
from models import BeerAvailability

class BeerRatingInline(admin.TabularInline):
    """ To enable inputting ratings manually when entering a beer.

    One day this should require only the foreign db id.
    """
    model = BeerRating
    extra = 1

class BeerAdmin(admin.ModelAdmin):
    """ Lets input ratings inline.
    """
    inlines = (BeerRatingInline,)
    list_display = ("name", "slug",)
    readonly_fields = ("slug", )

admin.site.register(Beer, BeerAdmin)
admin.site.register(BeerRating)
admin.site.register(BeerRater)

class AlkoLocationAdmin(admin.ModelAdmin):
    """ lets the slug be visible
    """
    readonly_fields=("slug",)
admin.site.register(AlkoLocation, AlkoLocationAdmin)
admin.site.register(BeerAvailability)
