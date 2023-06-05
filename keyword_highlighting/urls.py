from django.urls import path, include
from .views import *

urlpatterns = [
    path('kwh', view=home, name='kwh-home'),
    path('kwh/about/', view=about, name='kwh-about'),
]