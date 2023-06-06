from django.contrib import admin
from blog.models import Post, Like, Comment, Friend, Notification, FriendRequest

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Friend)
admin.site.register(Notification)
admin.site.register(FriendRequest)