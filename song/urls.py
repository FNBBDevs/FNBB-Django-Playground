from django.urls import path, include
from .views import *

urlpatterns = [
    path('song/', view=home, name='song-home'),
    path('song/about', view=about, name='song-about'),
    path('song/file/upload', view=upload_file, name='song-file-upload'),
    path('song/view_tables', view=view_tables, name='song-view-tables')
]