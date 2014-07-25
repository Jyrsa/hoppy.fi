# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Beer.alko_product_id'
        db.add_column(u'beerstatus_beer', 'alko_product_id',
                      self.gf('django.db.models.fields.CharField')(default='222222', max_length=6),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Beer.alko_product_id'
        db.delete_column(u'beerstatus_beer', 'alko_product_id')


    models = {
        u'beerstatus.alkolocation': {
            'Meta': {'object_name': 'AlkoLocation'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'beerstatus.beer': {
            'Meta': {'object_name': 'Beer'},
            'abv': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alko_product_id': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ibu': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"})
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
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"})
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