import django_filters
from django_filters import FilterSet
from .models import Song, ArtistStat, TrackStat, AlbumStat
from django.db.models import Q

class SongFilter(FilterSet):

    query = django_filters.CharFilter(method="query_filter", label="Search Tracks, Albums, or Artists")

    class Meta:
        model = Song
        fields = ["query"]
    
    def query_filter(self, queryset, name, value):
        return queryset.filter(
            Q(track__icontains=value) |
            Q(artist__icontains=value) |
            Q(album__icontains=value)
        )

class ArtistStatFilter(FilterSet):
    
    query = django_filters.CharFilter(method="query_filter", label="Search for Aritst")

    class Meta:
        model = ArtistStat
        fields = ["query"]

    def query_filter(self, queryset, name, value):
        return queryset.filter(
            Q(artist__icontains=value)
        )
    

class TrackStatFilter(FilterSet):
    
    query = django_filters.CharFilter(method="query_filter", label="Search for Track")

    class Meta:
        model = TrackStat
        fields = ["query"]

    def query_filter(self, queryset, name, value):
        return queryset.filter(
            Q(track__icontains=value)
        )
    

class AlbumStatFilter(FilterSet):
    
    query = django_filters.CharFilter(method="query_filter", label="Search for Album")

    class Meta:
        model = AlbumStat
        fields = ["query"]

    def query_filter(self, queryset, name, value):
        return queryset.filter(
            Q(album__icontains=value)
        )