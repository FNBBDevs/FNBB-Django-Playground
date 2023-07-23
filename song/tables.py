import django_tables2 as tables
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .filters import SongFilter

from .models import Song, ArtistStat, TrackStat, AlbumStat

class SongTable(tables.Table):
    track = tables.Column()
    artist = tables.Column()
    album = tables.Column()
    time = tables.Column()
    date = tables.Column()

    class Meta:
        model = Song

class FilteredSongView(SingleTableMixin, FilterView):
    table_class = SongTable
    model = Song
    template_name = "song/table.html"

    filterset_class = SongFilter

class ArtistStatsTable(tables.Table):
    artist = tables.Column()
    plays = tables.Column()
    total_time = tables.Column()

    class Meta:
        model = ArtistStat

class TrackStatsTable(tables.Table):
    track = tables.Column()
    plays = tables.Column()
    total_time = tables.Column()

    class Meta:
        model = TrackStat

class AlbumStatsTable(tables.Table):
    album = tables.Column()
    plays = tables.Column()
    total_time = tables.Column()

    class Meta:
        model = AlbumStat

