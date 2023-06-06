from django.urls import path

from .views import *

urlpatterns = [
    path('blog/', view=welcome, name='blog-welcome'),
    path('blog/welcome/', view=welcome, name='blog-welcome'),
    path('blog/about/', view=about, name='blog-about'),
    path('blog/home/', view=home, name='blog-home'),
    path('blog/post/create/', view=create_post, name='post-create'),
    path('blog/post/<int:key>/update', view=update_post, name='post-update'),
    path('blog/post/<int:key>/delete', view=delete_post, name='post-delete'),
    path('blog/post/<int:key>/like', view=like_post, name='post-like'),
    path('blog/post/<int:key>/view', view=view_post, name='post-view'),
    path('blog/comment/<int:commentkey>/<int:postkey>/update', view=update_comment, name='comment-update'),
    path('blog/comment/<int:commentkey>/<int:postkey>/delete', view=delete_comment, name='comment-delete'),
    path('blog/user/<int:key>/view', view=view_user, name='view-user'),
    path('blog/notification/<int:key>/view', view=clear_notification, name='notification-view'),
    path('blog/search/', view=search, name='search'),
    path('blog/autocomplete/', view=autocomplete_search, name='autocomplete'),
    path('blog/friend/<int:key>/add', view=add_friend, name='friend-add'),
    path('blog/friend/<int:key>/remove', view=remove_friend, name='friend-remove'),
]