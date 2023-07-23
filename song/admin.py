from django.contrib import admin
from song.models import Song, ArtistStat, TrackStat, AlbumStat

# Register your models here.
admin.site.register(Song)
admin.site.register(ArtistStat)
admin.site.register(TrackStat)
admin.site.register(AlbumStat)
