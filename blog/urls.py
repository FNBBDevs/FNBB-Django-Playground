from django.urls import path

from .views import *

urlpatterns = [
    path('', view=welcome, name='blog-welcome'),
    path('welcome/', view=welcome, name='blog-welcome'),
    path('about/', view=about, name='blog-about'),
    path('home/', view=home, name='blog-home'),
    path('post/create/', view=create_post, name='post-create'),
    path('post/<int:key>/update', view=update_post, name='post-update'),
    path('post/<int:key>/delete', view=delete_post, name='post-delete'),
    path('post/<int:key>/like', view=like_post, name='post-like'),
    path('post/<int:key>/view', view=view_post, name='post-view'),
    path('comment/<int:commentkey>/<int:postkey>/update', view=update_comment, name='comment-update'),
    path('comment/<int:commentkey>/<int:postkey>/delete', view=delete_comment, name='comment-delete'),
    path('user/<int:key>/view', view=view_user, name='view-user'),
    path('notification/<int:key>/view', view=clear_notification, name='notification-view'),
    path('search/', view=search, name='search'),
    path('autocomplete/', view=autocomplete_search, name='autocomplete')
]