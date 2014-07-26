# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'AlkoLocation', fields ['store_id']
        db.delete_unique(u'beerstatus_alkolocation', ['store_id'])


    def backwards(self, orm):
        # Adding unique constraint on 'AlkoLocation', fields ['store_id']
        db.create_unique(u'beerstatus_alkolocation', ['store_id'])


    models = {
        u'beerstatus.alkolocation': {
            'Meta': {'object_name': 'AlkoLocation'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '24.934792'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '60.170814'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'store_id': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'beerstatus.beer': {
            'Meta': {'object_name': 'Beer'},
            'abv': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alko_product_id': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ebu': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'ibu': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0.33'})
        },
        u'beerstatus.beeravailability': {
            'Meta': {'object_name': 'BeerAvailability'},
            'beer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beerstatus.Beer']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beerstatus.AlkoLocation']"})
        },
        u'beerstatus.beerrater': {
            'Meta': {'object_name': 'BeerRater'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'url_base': ('django.db.models.fields.CharField', [], {'default': "'http://localhost/?q=%s'", 'max_length': '400'})
        },
        u'beerstatus.beerrating': {
            'Meta': {'unique_together': "(('beer', 'rater'),)", 'object_name': 'BeerRating'},
            'beer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beerstatus.Beer']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'foreign_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rater': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beerstatus.BeerRater']"}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['beerstatus']