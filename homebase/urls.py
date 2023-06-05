from django.urls import path, include
from .views import *

urlpatterns = [
    path('', view=home, name='homebase-home'),
    path('homebase', view=home, name='homebase-home'),
    path('homebase/about/', view=about, name='homebase-about'),
    path('', include('keyword_highlighting.urls')),
    path('', include('blog.urls')),
]