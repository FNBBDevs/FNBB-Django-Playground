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
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}_liked_post_{self.post}"

class Comment(models.Model):
    key     = models.AutoField(primary_key=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = TextField(default='')
    date    = DateTimeField(default=datetime.datetime.now())
    edited  = IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}_commented_on_post_{self.post}"
    

class Friend(models.Model):
    key          = models.AutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_user')
    friends_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    since        = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f"{self.user.username} & {self.friend.username}"
    
class Notification(models.Model):
    LIKE_NOTIFICATION           = 'LIKE NOTIFICATION'
    COMMENT_NOTIFICATION        = 'COMMENT NOTIFICATION'
    FRIEND_REQUEST_NOTIFICATION = 'FRIEND REQUEST NOTIFICATION'
    STANDARD_NOTIFICATION       = 'STANDARD NOTIFICATION'

    NOTIFICATION_TYPES = (
        (LIKE_NOTIFICATION, 'Like Notification'),
        (COMMENT_NOTIFICATION, 'Comment Notification'),
        (FRIEND_REQUEST_NOTIFICATION, 'Friend Request Notification'),
        (STANDARD_NOTIFICATION, 'Notification')
    )

    key  = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user', default=6)
    user_to_notify = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user_to_notify', default=6)
    notification_type = models.CharField(max_length=30, default=STANDARD_NOTIFICATION, choices=NOTIFICATION_TYPES)
    content = models.TextField(default='')
    viewed = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.datetime.now())
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.key}_{self.user.username}_{self.notification_type}"

