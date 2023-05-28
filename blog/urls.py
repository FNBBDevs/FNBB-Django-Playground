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
    path('post/<int:key>/like', views.like, name='post-like')
]