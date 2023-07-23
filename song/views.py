from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
import json
from .models import Song, ArtistStat, TrackStat, AlbumStat
from .tables import SongTable, ArtistStatsTable, TrackStatsTable, AlbumStatsTable
from .filters import SongFilter, ArtistStatFilter, TrackStatFilter, AlbumStatFilter
from django_tables2 import RequestConfig
from django.http import JsonResponse

TRACK = "master_metadata_track_name"
ARTIST = "master_metadata_album_artist_name"
ALBUM = "master_metadata_album_album_name"
TIME = "ms_played"
DATE = "ts"

def home(request):
    template = "song/home.html"
    title = "Home"
    return render(request, template_name=template, context={"title": title})

def about(request):
    template = "song/about.html"
    title = "About"
    return render(request, template_name=template, context={"title":title})

@login_required
def upload_file(request):
    global PRE_SEARCH_FILE
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                payload = json.loads(request.FILES['file'].read().decode('UTF-8'))

                for song in payload:
                    song_title = song[TRACK]
                    song_artist = song[ARTIST]
                    song_album = song[ALBUM]
                    song_time = song[TIME]
                    song_date = song[DATE]

                    if not song_title:
                        song_title = "No Track"
                    if not song_artist:
                        song_artist = "No Artist"
                    if not song_album:
                        song_album = "No Album"
                    if not song_time:
                        song_time = 0
                    if not song_date:
                        song_date = ""

                    s = Song(
                        date = song_date,
                        track = song_title,
                        artist = song_artist,
                        album = song_album,
                        time = song_time
                    )

                    s.save()

                return redirect("song-home")
            except Exception as exception:
                messages.warning(request, "A problem was encountered. Could not process file.")
                messages.warning(request, f"Additional information: {exception}")
                return redirect('song-home')
        else:
            messages.warning(request, "The form was not valid!")
            return redirect('song-home')
    else:
        form = UploadFileForm()
        template = "song/file_upload.html"
        context = {
            'title': 'Upload File',
            'form': form
        }

        return render(request, template_name=template, context=context)

@login_required
def view_tables(request):
    title = "Listening History"
    template = "song/table.html"

    songs = Song.objects.all()
    myFilter = SongFilter(request.GET, queryset=songs)
    songs = myFilter.qs
    table = SongTable(songs)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)

    return render(request, template_name=template, context={"title": title, "table":table, "myFilter":myFilter})

@login_required
def view_artist_stats(request):
    title = "Artist Stats"
    template = "song/artist_stats.html"

    artists = ArtistStat.objects.all()
    myFilter = ArtistStatFilter(request.GET, queryset=artists)
    artists = myFilter.qs
    table = ArtistStatsTable(artists)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)

    return render(request, template_name=template, context={"title":title, "table": table, "myFilter":myFilter})

@login_required
def view_track_stats(request):
    title = "Track Stats"
    template = "song/track_stats.html"

    tracks = TrackStat.objects.all()
    myFilter = TrackStatFilter(request.GET, queryset=tracks)
    tracks = myFilter.qs
    table =TrackStatsTable(tracks)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)

    return render(request, template_name=template, context={"title":title, "table": table, "myFilter":myFilter})

@login_required
def view_album_stats(request):
    title = "Album Stats"
    template = "song/album_stats.html"

    albums = AlbumStat.objects.all()
    myFilter = AlbumStatFilter(request.GET, queryset=albums)
    albums = myFilter.qs
    table = AlbumStatsTable(albums)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)

    return render(request, template_name=template, context={"title":title, "table": table, "myFilter":myFilter})

@login_required
def autocomplete_search(request):
    query = request.GET.get('query')
    query_on = request.GET.get('type')

    if query:
        if query_on == "artist":
            artists = list(set([artist_stat.artist for artist_stat in ArtistStat.objects.all().filter(artist__icontains=query)]))
            return JsonResponse({"status":200, "data": artists})
        elif query_on == "track":
            tracks = list(set([track_stat.track for track_stat in TrackStat.objects.all().filter(track__icontains=query)]))
            return JsonResponse({"status":200, "data": tracks})
        elif query_on == "album":
            albums = list(set([album_stat.album for album_stat in AlbumStat.objects.all().filter(album__icontains=query)]))
            return JsonResponse({"status":200, "data": albums})
        elif query_on == "listen":
            tracks = list(set([song.track for song in Song.objects.all().filter(track__icontains=query)]))
            artists = list(set([song.artist for song in Song.objects.all().filter(artist__icontains=query)]))
            albums = list(set([song.album for song in Song.objects.all().filter(album__icontains=query)]))
            return JsonResponse({'status': 200, 'data': tracks + artists + albums})
    return JsonResponse({"status":200, "data":[]})

@login_required
def artist_stats_build(request):
    songs = Song.objects.all()

    artists = {}

    for song in songs:
        if song.artist in artists:
            artists[song.artist]["played"] += 1
            artists[song.artist]["time_listened"] += song.time
        else:
            artists[song.artist] = {"played": 1, "time_listened": song.time}

    artists = [{"artist":artist, "hits":artists[artist]["played"], "totaltime":artists[artist]["time_listened"] / 600000} for artist in artists]

    for artist in artists:
        artist, hits, totaltime = artist.values()
        AS = ArtistStat(
            artist=artist,
            plays=hits,
            total_time=totaltime
        )
        AS.save()
    
    messages.success(request, "Artist Stats built successfully")
    return redirect('song-home')

@login_required
def track_stats_build(request):
    songs = Song.objects.all()

    tracks = {}

    for song in songs:
        if song.track in tracks:
            tracks[song.track]["played"] += 1
            tracks[song.track]["time_listened"] += song.time
        else:
            tracks[song.track] = {"played": 1, "time_listened": song.time}

    tracks = [{"track":track, "hits":tracks[track]["played"], "totaltime":tracks[track]["time_listened"] / 600000} for track in tracks]

    for track in tracks:
        track, hits, totaltime = track.values()
        AS = TrackStat(
            track=track,
            plays=hits,
            total_time=totaltime
        )
        AS.save()
    
    messages.success(request, "Track Stats built successfully")
    return redirect('song-home')

@login_required
def album_stats_build(request):
    songs = Song.objects.all()

    albums = {}

    for song in songs:
        if song.album in albums:
            albums[song.album]["played"] += 1
            albums[song.album]["time_listened"] += song.time
        else:
            albums[song.album] = {"played": 1, "time_listened": song.time}

    albums = [{"album":album, "hits":albums[album]["played"], "totaltime":albums[album]["time_listened"] / 600000} for album in albums]

    for album in albums:
        album, hits, totaltime = album.values()
        AS = AlbumStat(
            album=album,
            plays=hits,
            total_time=totaltime
        )
        AS.save()
    
    messages.success(request, "Album Stats built successfully")
    return redirect('song-home')

@login_required
def delete_stats(request):
    stats1 = ArtistStat.objects.all()
    stats2 = TrackStat.objects.all()
    stats3 = AlbumStat.objects.all()

    def del_these_stats(stats):
        for stat in stats:
            stat.delete()
    
    del_these_stats(stats1)
    del_these_stats(stats2)
    del_these_stats(stats3)

    return redirect('song-home')