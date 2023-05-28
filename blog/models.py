from django.db import models
from django.db.models.fields import TextField, EmailField, IntegerField, DateTimeField
import datetime

# Create your models here.
class Post(models.Model):
    key     = models.AutoField(primary_key=True)
    date    = DateTimeField(default=datetime.datetime.now())
    author  = TextField(default='')
    title   = TextField(default='')
    content = TextField(default='')
    likes   = IntegerField(default=0)

    def __str__(self):
        return self.title

class Like(models.Model):
    key = models.AutoField(primary_key=True)
    post = IntegerField(default=-1)
    user = TextField(default='')

