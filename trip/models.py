# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class Activity(models.Model):
    actid = models.BigIntegerField(unique=True, db_column='ActID') # Field name made lowercase.
    name = models.CharField(max_length=300, db_column='Name', blank=True) # Field name made lowercase.
    placeid = models.BigIntegerField(null=True, db_column='PlaceID', blank=True) # Field name made lowercase.
    duration = models.IntegerField(null=True, db_column='Duration', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tblActivities'

class Note(models.Model):
    note_id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=150)
    media_path = models.CharField(max_length=600, blank=True)
    title = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(null=True, max_digits=7, decimal_places=3, blank=True)
    longitude = models.DecimalField(null=True, max_digits=7, decimal_places=3, blank=True)
    poi_id = models.BigIntegerField(null=True, blank=True)
    place_id = models.BigIntegerField(null=True, blank=True)
    trip_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    note_source = models.CharField(max_length=150)
    metadata = models.TextField(blank=True)
    class Meta:
        db_table = u'tbl_notes'

class Place(models.Model):
    place_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=600)
    country = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    rating = models.IntegerField()
    latitude = models.DecimalField(max_digits=7, decimal_places=3)
    longitude = models.DecimalField(max_digits=7, decimal_places=3)
    img_src = models.CharField(max_length=300)
    metadata = models.TextField()
    class Meta:
        db_table = u'tbl_place'

class POI(models.Model):
    poi_id = models.BigIntegerField(primary_key=True)
    place_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    latitude = models.DecimalField(null=True, max_digits=7, decimal_places=3, blank=True)
    longitude = models.DecimalField(null=True, max_digits=7, decimal_places=3, blank=True)
    title = models.CharField(max_length=300, blank=True)
    type = models.CharField(max_length=300, blank=True)
    img_src = models.CharField(max_length=300, blank=True)
    extern_url = models.TextField(blank=True)
    metadata = models.TextField(blank=True)
    class Meta:
        db_table = u'tbl_poi'

class TimelineEvent(models.Model):
    event_id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=300)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    poi_id = models.BigIntegerField(null=True, blank=True)
    place_id = models.BigIntegerField(null=True, blank=True)
    metadata = models.TextField(blank=True)
    class Meta:
        db_table = u'tbl_timeline_event'

class Travlog(models.Model):
    travlog_id = models.BigIntegerField()
    title = models.CharField(max_length=600)
    sub_title = models.CharField(max_length=600, blank=True)
    create_ts = models.DateTimeField()
    trip_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    public_link = models.CharField(max_length=600, blank=True)
    html_text = models.TextField(blank=True)
    metadata = models.TextField(blank=True)
    class Meta:
        db_table = u'tbl_travlog'

class Trip(models.Model):
    trip_id = models.BigIntegerField(primary_key=True)
    origin_id = models.BigIntegerField()
    dest_id = models.BigIntegerField()
    owner_id = models.BigIntegerField()
    status = models.CharField(max_length=150)
    mode = models.CharField(max_length=300, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=600, blank=True)
    description = models.TextField(blank=True)
    metadata = models.TextField(blank=True)
    class Meta:
        db_table = u'tbl_trip'

