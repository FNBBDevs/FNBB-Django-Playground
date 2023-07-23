from django.urls import path, include
from django.urls import re_path as url
from .views import *
from .models import Song
from dal import autocomplete

urlpatterns = [
    path('song/', view=home, name='song-home'),
    path('song/about', view=about, name='song-about'),
    path('song/file/upload', view=upload_file, name='song-file-upload'),
    path('song/listening_history', view=view_tables, name='song-listening-history'),
    path('song/stats/autocomplete', view=autocomplete_search, name='autocomplete'),
    path('song/stats/artist', view=view_artist_stats, name='song-artist-stats'),
    path('song/stats/track', view=view_track_stats, name='song-track-stats'),
    path('song/stats/album', view=view_album_stats, name='song-album-stats'),
    path('song/stats/artist/build', view=artist_stats_build, name='song-artist-stats-build'),
    path('song/stats/track/build', view=track_stats_build, name='song-track-stats-build'),
    path('song/stats/album/build', view=album_stats_build, name='song-album-stats-build'),
    path('song/stats/delete', view=delete_stats, name='song-stats-delete'),
]