from django.contrib import admin
from blog.models import Post, Like, Comment, Friend

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Friend)