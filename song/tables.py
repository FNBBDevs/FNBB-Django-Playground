import django_tables2 as tables

from .models import Song

class SongTable(tables.Table):
    track = tables.Column()
    artist = tables.Column()
    album = tables.Column()
    time = tables.Column()
    date = tables.Column()

    class Meta:
        model = Song