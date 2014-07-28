from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from tastypie.api import Api
from beerstatus.api import AlkoLocationResource
from beerstatus.api import BeerResource
from beerstatus.api import BeerRaterResource
from beerstatus.api import BeerRatingResource
from beerstatus.api import BeerAvailabilityResource

api_v1 = Api(api_name="v1")
api_v1.register(AlkoLocationResource())
api_v1.register(BeerResource())
api_v1.register(BeerRatingResource())
api_v1.register(BeerRaterResource())
api_v1.register(BeerAvailabilityResource())



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hoppy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(api_v1.urls)),
    url(r'^beerstatus/', include('beerstatus.urls')),
)

