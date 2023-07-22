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
    