from django.db import models
from django.db.models.fields import TextField, EmailField, IntegerField, DateTimeField
from django.contrib.auth.models import User

import datetime

class Post(models.Model):
    key      = models.AutoField(primary_key=True)
    date     = DateTimeField(default=datetime.datetime.now())
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = TextField(default='')
    content  = TextField(default='')
    likes    = IntegerField(default=0)
    comments = IntegerField(default=0)

    def __str__(self):
        return self.title

class Like(models.Model):
    key  = models.AutoField(primary_key=True)
    post = IntegerField(default=-1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}_liked_post_{self.post}"

class Comment(models.Model):
    key     = models.AutoField(primary_key=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = IntegerField(default=-1)
    comment = TextField(default='')
    date    = DateTimeField(default=datetime.datetime.now())
    edited  = IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}_commented_on_post_{self.post}"

