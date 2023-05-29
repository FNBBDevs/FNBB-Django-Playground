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
    key  = models.AutoField(primary_key=True)
    post = IntegerField(default=-1)
    user = TextField(default='')

    def __str__(self):
        return f"{self.user}_liked_post_{self.post}"

class Comment(models.Model):
    key     = models.AutoField(primary_key=True)
    post    = IntegerField(default=-1)
    user    = TextField(default='')
    comment = TextField(default='')
    date    = DateTimeField(default=datetime.datetime.now())
    edited  = IntegerField(default=0)

    def __str__(self):
        return f"{self.user}_commented_on_post_{self.post}"

