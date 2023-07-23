from django.db import models
from django.db.models.fields import TextField, EmailField, IntegerField, DateTimeField
from django.contrib.auth.models import User

import datetime

class Song(models.Model):
    key      = models.AutoField(primary_key=True)
    date     = DateTimeField(default=datetime.datetime.now())
    track    = TextField(default="No Track")
    artist   = TextField(default="No Artist")
    time     = IntegerField(default=0)
    album    = TextField(default="No Album")

    def __str__(self):
        return f"{self.artist} - {self.track}"

class ArtistStat(models.Model):
    key = models.AutoField(primary_key=True)
    artist = TextField(default="No Artist")
    plays = IntegerField(default=0)
    total_time = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)

    def __str__(self):
        return self.artist

class TrackStat(models.Model):
    key = models.AutoField(primary_key=True)
    track = TextField(default="No Track")
    plays = IntegerField(default=0)
    total_time = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)

    def __str__(self):
        return self.track
    
class AlbumStat(models.Model):
    key = models.AutoField(primary_key=True)
    album = TextField(default="No Album")
    plays = IntegerField(default=0)
    total_time = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)

    def __str__(self):
        return self.album

    