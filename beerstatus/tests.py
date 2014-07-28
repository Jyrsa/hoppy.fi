from django.test import TestCase

# Create your tests here.

from models import Beer
from models import BeerRater
from models import AlkoLocation

from tastypie.test import ResourceTestCase

class APIV1Test(ResourceTestCase):
    
    fixtures = ['beerdata_simple.json']

    def setUp(self):
        super(APIV1Test, self).setUp()
            
        self.karhu = Beer.objects.get(pk=1)
        self.olvi = Beer.objects.get(pk=2)
        self.lahden = Beer.objects.get(pk=3)
        self.alko = AlkoLocation.objects.get(pk=1)

        self.ratebeer = BeerRater.objects.get(pk=1)

        self.olvi_rating = self.ratebeer.get_rating_for(self.olvi)
        self.lahden_rating = self.ratebeer.get_rating_for(self.lahden)
        self.karhu_rating = self.ratebeer.get_rating_for(self.karhu)
        
        self.alko_list_url = '/api/v1/alko/'

    def test_get_alko_list(self):
        resp = self.api_client.get('/api/v1/alko/', format='json')
        self.assertValidJSONResponse(resp)
        response = self.deserialize(resp)
        self.assertEqual(len(response["objects"]), 1) 
        testalko = response["objects"][0]
        self.assertEqual(testalko["id"], self.alko.pk)
        self.assertEqual(testalko["slug"], self.alko.slug)
        self.assertIsNone(testalko.get("last_modified", None))
        self.assertIsNone(testalko.get("created_at", None))

    def test_get_beer_list(self):
        resp = self.api_client.get('/api/v1/beer/', format='json')
        self.assertValidJSONResponse(resp)
        response = self.deserialize(resp)
        #nonactive lahden erikoinen should be filtered
        self.assertEqual(len(response["objects"]), 2) 
        karhu = response["objects"][0]
        self.assertEqual(karhu["id"], self.karhu.pk)
        self.assertEqual(karhu["slug"], self.karhu.slug)
        self.assertIsNone(karhu.get("last_modified", None))
        self.assertIsNone(karhu.get("created_at", None))
        
        olvi = response["objects"][1]
        self.assertEqual(olvi["id"], self.olvi.pk)
        self.assertEqual(olvi["slug"], self.olvi.slug)
        self.assertIsNone(olvi.get("last_modified", None))
        self.assertIsNone(olvi.get("created_at", None))

    def test_get_beer_info_and_rating(self):
        resp = self.api_client.get('/api/v1/beer/%d/' % self.karhu.pk, format='json')
        self.assertValidJSONResponse(resp)
        response = self.deserialize(resp)
        self.assertEqual(response["id"], self.karhu.pk)
        self.assertEqual(response["style"], self.karhu.style)
        rating = response["scores"][0]

        self.assertEqual(rating["rater"], self.ratebeer.name)
        self.assertEqual(rating["score"], self.karhu_rating.rating)
        self.assertEqual(
                        rating["url"],
                        self.ratebeer.get_url(self.karhu_rating.foreign_id)
                        )

#ToDo: BDD tests for scraping functionality

