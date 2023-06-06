from django.urls import path, include
from .views import *

urlpatterns = [
    path('kwh', view=home, name='kwh-home'),
    path('kwh/about/', view=about, name='kwh-about'),
    path('kwh/file/upload', view=upload_file, name='kwh-upload'),
    path('kwh/file/view', view=view_file, name='kwh-view')
]