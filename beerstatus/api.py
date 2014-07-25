from tastypie.resources import ModelResource
from tastypie.resources import ALL
from tastypie.resources import ALL_WITH_RELATIONS

from tastypie import fields
from models import AlkoLocation
from models import Beer
from models import BeerRating
from models import BeerAvailability
from models import BeerRater

from util import PrettyJSONSerializer
from django.conf import settings

class AlkoLocationResource(ModelResource):

    slug = fields.CharField(attribute="slug")

    class Meta:
        queryset = AlkoLocation.objects.all()
        resource_name = "alko"
        filtering = {
        'pk': ALL_WITH_RELATIONS,
        'store_id': ALL_WITH_RELATIONS,
        'slug': ALL_WITH_RELATIONS
        }
        excludes = ["last_modified", "created_at"]
        if settings.DEBUG:
            serializer = PrettyJSONSerializer()



class BeerRatingResource(ModelResource):
    class Meta:
        queryset = BeerRating.objects.all()
        resource_name = "rateit"
        filtering = {'pk': ALL_WITH_RELATIONS}
    

class BeerRaterResource(ModelResource):
    class Meta:
        queryset = BeerRater.objects.all()
        resource_name = "rater"
        filtering = {'pk': ALL_WITH_RELATIONS}



class BeerResource(ModelResource):
    scores = fields.ListField(readonly=True)
    slug = fields.CharField(attribute="slug")

    def dehydrate_scores(self, bundle):
        list_ = []
        for rater in BeerRater.objects.all():
            rating = BeerRating.objects.get(beer=bundle.obj, rater=rater)
            list_.append({
                            "rater": rater.name, 
                            "score": rating.rating,
                            "url": rater.get_url(rating.foreign_id)
                            })
        return list_

    class Meta:
        queryset = Beer.objects.filter(active=True)
        resource_name = "beer"
        filtering ={
                'pk': ALL_WITH_RELATIONS,
                'ratings': ALL
                }
        excludes = ["last_modified", "created_at"]
        if settings.DEBUG:
            serializer = PrettyJSONSerializer()

class BeerAvailabilityResource(ModelResource):
    beer = fields.ForeignKey(BeerResource, "beer", full=True)
    location = fields.ForeignKey(AlkoLocationResource, "location")
    class Meta:
        queryset = BeerAvailability.objects.all()
        resource_name = "availability"
        filtering = {
            'location': ALL_WITH_RELATIONS, 
            'date': ['exact', 'gt']
            }
        excludes = ["last_modified", "created_at"]
        if settings.DEBUG:
            serializer = PrettyJSONSerializer()

    def get_object_list(self, request):
        vval = super(BeerAvailabilityResource,
                        self).get_object_list(request)
        latest = vval.dates('date', 'day', order="DESC")[0]
        return super(BeerAvailabilityResource,
                    self).get_object_list(request).filter(
                    date=latest 
                    )
 
        return vval


