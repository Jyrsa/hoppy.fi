# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Beer'
        db.create_table(u'beerstatus_beer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('ibu', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('abv', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'beerstatus', ['Beer'])

        # Adding model 'BeerRater'
        db.create_table(u'beerstatus_beerrater', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'beerstatus', ['BeerRater'])

        # Adding model 'BeerRating'
        db.create_table(u'beerstatus_beerrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['beerstatus.Beer'])),
            ('rater', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['beerstatus.BeerRater'])),
            ('foreign_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('rating', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'beerstatus', ['BeerRating'])

        # Adding unique constraint on 'BeerRating', fields ['beer', 'rater']
        db.create_unique(u'beerstatus_beerrating', ['beer_id', 'rater_id'])

        # Adding model 'AlkoLocation'
        db.create_table(u'beerstatus_alkolocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('address', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'beerstatus', ['AlkoLocation'])

        # Adding model 'BeerAvailability'
        db.create_table(u'beerstatus_beeravailability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['beerstatus.Beer'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['beerstatus.AlkoLocation'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'beerstatus', ['BeerAvailability'])


    def backwards(self, orm):
        # Removing unique constraint on 'BeerRating', fields ['beer', 'rater']
        db.delete_unique(u'beerstatus_beerrating', ['beer_id', 'rater_id'])

        # Deleting model 'Beer'
        db.delete_table(u'beerstatus_beer')

        # Deleting model 'BeerRater'
        db.delete_table(u'beerstatus_beerrater')

        # Deleting model 'BeerRating'
        db.delete_table(u'beerstatus_beerrating')

        # Deleting model 'AlkoLocation'
        db.delete_table(u'beerstatus_alkolocation')

        # Deleting model 'BeerAvailability'
        db.delete_table(u'beerstatus_beeravailability')


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