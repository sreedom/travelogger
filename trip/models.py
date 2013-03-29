from django.db import models

# Create your models here.

class User(models.Model):
    UserId = models.IntegerField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    EmailAddress = models.CharField(max_length=100)
    LoginPassword = models.CharField(max_length=100)
    Badges = models.TextField() #json list of badge_ids
    class Meta:
        db_table = 'tblUsers'

class Place(models.Model):
    PlaceId = models.IntegerField(primary_key=True)
    DisplayName  = models.CharField(max_length=100)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    ParentReqionID = models.IntegerField()
    Tags = models.TextField()

    class Meta:
        db_table = 'tblPlaces'

class Resource(models.Model):
    PlaceID = models.IntegerField()
    ResType = models.CharField(max_length=30)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Data = models.TextField()

    class Meta:
        db_table = u'tblResources'

class Activities(models.Model):
    ActID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    PlaceID = models.IntegerField()
    Duration = models.IntegerField()

    class Meta:
        db_table = u'tblActivities'



class LogEntry(models.Model):
    UserID = models.IntegerField()
    TripID = models.IntegerField()
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    LogTime = models.DateTimeField()
    LogType = models.CharField(max_length=30)
    Data = models.TextField()

    class Meta:
        db_table = u'tblLogs'

class Trip:
    TripID = models.IntegerField()
    DisplayName = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)
    StartDate = models.DateField()
    EndDate  = models.DateField()
    Itinerary = models.TextField()
    class Meta:
        db_table = u'tblTrips'