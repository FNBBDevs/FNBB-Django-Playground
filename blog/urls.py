from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='blog-welcome'),
    path('welcome/', views.welcome, name='blog-welcome'),
    path('about/', views.about, name='blog-about'),
    path('home/', views.home, name='blog-home'),
    path('create/', views.create_post, name='blog-create'),
    path('post/<int:key>/update', views.update, name='post-update'),
    path('post/<int:key>/delete', views.delete, name='post-delete'),
    path('post/<int:key>/like', views.like, name='post-like'),
    path('post/<int:key>/view', view=views.view_post, name='post-view'),
    path('comment/<int:commentkey>/<int:postkey>/update', view=views.update_comment, name='comment-update'),
    path('comment/<int:commentkey>/<int:postkey>/delete', view=views.delete_comment, name='comment-delete'),
]